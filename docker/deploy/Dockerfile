FROM opentarock/server-users-base

MAINTAINER The OpenTarock Project

ADD . /project
WORKDIR project

RUN python3 setup.py install
WORKDIR /
RUN rm -rf project

ENTRYPOINT ["server-users"]
