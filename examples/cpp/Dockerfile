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

RUN apt-get install -y curl tzdata
RUN curl -sSL "https://github.com/facebook/infer/releases/download/v0.17.0/infer-linux64-v0.17.0.tar.xz" \
	| tar -C /opt -xJ && \
	ln -s "/opt/infer-linux64-v0.17.0/bin/infer" /usr/local/bin/infer


RUN apt-get install -y python

RUN cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 . && make
RUN infer run --compilation-database compile_commands.json

CMD ["./example"]