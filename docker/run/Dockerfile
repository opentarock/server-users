FROM opentarock/server-users-base

MAINTAINER The OpenTarock Project

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /project

RUN mkdir /sqlite

WORKDIR /project

CMD ["bash", "scripts/run_server.sh"]
