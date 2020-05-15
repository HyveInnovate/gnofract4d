FROM ubuntu:18.04

ENV TZ=GMT
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y build-essential git cmake autoconf libtool pkg-config libpng-dev libjpeg-dev
RUN apt-get install -y libmpfr-dev libgmp-dev

WORKDIR /src

ARG main_source
ARG formula_source
ARG gmp_support

COPY examples/cpp/${main_source} ./main.cpp
COPY examples/cpp/CMakeLists.txt ./
COPY fract4d/c/fract_stdlib.cpp fract4d/c/fract_stdlib.h fract4d/c/pf.h  ./
COPY fract4d/c/model/ ./model
COPY ${formula_source} ./

ENV formula_source=$formula_source
ENV gmp_support=$gmp_support
COPY examples/cpp/mp_double.h ./mp_double.h

RUN apt-get install -y curl tzdata python
ADD https://github.com/facebook/infer/releases/download/v0.17.0/infer-linux64-v0.17.0.tar.xz infer-linux64-v0.17.0.tar.xz
RUN tar -xf infer-linux64-v0.17.0.tar.xz -C /opt && \
	ln -s "/opt/infer-linux64-v0.17.0/bin/infer" /usr/local/bin/infer

ADD https://sourceware.org/pub/valgrind/valgrind-3.15.0.tar.bz2 valgrind-3.15.0.tar.bz2
RUN tar -xjf valgrind-3.15.0.tar.bz2 -C /opt && \
	cd /opt/valgrind-3.15.0 && ./configure && make && make install

# todo: ADD url is not caching properly so we need to change that into something like "CMD test destination || curl URL --output destination"

RUN cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 . && make
RUN infer run --compilation-database compile_commands.json

RUN apt-get install -y libc6-dbg

CMD ["./example"]