FROM ubuntu:18.04

ENV TZ=Europe/Minsk
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y build-essential git cmake autoconf libtool pkg-config libpng-dev libjpeg-dev

RUN apt-get update && apt-get -y install git python3-pip
RUN python3 -m pip install ninja meson
RUN git clone --recurse-submodules --branch v1.0.0 https://github.com/DX-MON/crunch.git /opt/crunch
RUN cd /opt/crunch && meson build && ninja -C build install

WORKDIR /src

COPY test/CMakeLists.txt ./
COPY test/test.cpp ./
COPY fract_stdlib.cpp fract_stdlib.h pf.h  ./
COPY model/ ./model

RUN cmake . && make

# CMD ["crunch++ libtestrunner"]
