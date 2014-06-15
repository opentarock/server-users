FROM ubuntu:14.04

MAINTAINER The OpenTarock Project

RUN apt-get update
RUN apt-get -y install python3 python3-pip

RUN apt-get -y install curl git build-essential
RUN mkdir build

RUN pip3 install cython

# Build and install nanomsg
WORKDIR /build
RUN curl -O http://download.nanomsg.org/nanomsg-0.3-beta.tar.gz
RUN echo "547ad73ec4146e6ae70d5518748e6018 nanomsg-0.3-beta.tar.gz" > md5sum.txt
RUN md5sum -c md5sum.txt
RUN tar xvf nanomsg-0.3-beta.tar.gz
WORKDIR nanomsg-0.3-beta
RUN ./configure && \
    make && \
    make check && \
    make install

# Build and install capnproto
WORKDIR /build
RUN curl -O https://capnproto.org/capnproto-c++-0.4.1.tar.gz
RUN tar zxf capnproto-c++-0.4.1.tar.gz
WORKDIR capnproto-c++-0.4.1
RUN ./configure && \
    make check && \
    make install

# Clean up
WORKDIR /
RUN rm -rf build
