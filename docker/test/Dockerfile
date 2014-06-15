FROM opentarock/server-users-base

MAINTAINER The OpenTarock Project

RUN apt-get -y install \
    curl \
    git-core \
    build-essential \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev

RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
ENV PATH $HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH
RUN eval "$(pyenv init -)"

RUN pyenv install 3.3.5
RUN pyenv global system 3.3.5
RUN pyenv rehash

RUN pip3 install cython
RUN pip3.3 install cython

RUN pip3 install tox

WORKDIR /project

CMD ["tox"]
