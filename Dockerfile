FROM ubuntu:18.04
RUN apt-get -y update && apt-get -y install software-properties-common gcc

# Install binary rewriting tools
RUN add-apt-repository ppa:mhier/libboost-latest
RUN echo "deb [trusted=yes] https://grammatech.github.io/gtirb/pkgs/bionic ./" | tee -a /etc/apt/sources.list.d/gtirb.list
RUN apt-get -y update
RUN apt-get -y install libgtirb gtirb-pprinter ddisasm

# Rewrite test binaries
COPY . /DebloatingTestSuite
WORKDIR /DebloatingTestSuite
RUN find pytestbed -type f -executable -exec ddisasm --ir {}.gtirb {} \;
RUN find pytestbed -type f -executable -exec gtirb-pprinter {}.gtirb --binary {}-rewritten \;
RUN find pytestbed -name "*-rewritten"
