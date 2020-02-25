#!/usr/bin/ruby

#
# Assembles a program and returns true is the program executes and returns 42.
#

def run(asm)

  File.delete('temp.asm') if File.exists?('temp.asm')
  File.delete('temp.exe') if File.exists?('temp.exe')

  # Write the asm source

  File.open('temp.asm', 'w+') { |file|
    asm.each { |line| file.write(line) }
  }

  # Compile the asm source

  Kernel.system('nasm', '-f', 'bin', '-o', 'temp.exe', 'temp.asm') or
    raise "Failed to execute nasm"

  File.chmod(0755, 'temp.exe')

  # Execute the program

  Kernel.system('./temp.exe')

  File.delete('temp.asm') if File.exists?('temp.asm')
  File.delete('temp.exe') if File.exists?('temp.exe')

  return ($?.exitstatus == 42)
end

#
# Main
#

# Read the asm source

asm = nil

File.open('tiny.asm') { |file|
  asm = file.readlines
}

output = []

# Iterate over each line of the source

for i in 0..asm.length-1
  line = asm[i]
  puts line

  if (match = /^(.*?\sd(b|w|d)\s+)([^;]+)(;.*?)$/.match(line)) &&
                           !/AddressOfEntryPoint/.match(line)
    used = false

    [0, 1, 42, -1, -42].each { |num|
      asm[i] = "#{match[1]} #{num} #{match[4]}\n"

      # If the program fails to run, the field is in use
      if run(asm) == false
        used = true
        break
      end
    }

    # Restore the source line
    asm[i] = line

    # If the field is not used, add a comment
    if !used
      line = "#{match[0]} UNUSED\n"
      puts "UNUSED"
    end
  end

  # Add the line to the output array
  output.push line
end

# Write the output to unused.asm

File.open('unused.asm', 'w+') { |file|
  output.each { |line| file.write(line) }
}

puts "Output written to unused.asm"
