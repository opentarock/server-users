#!/usr/bin/env bash

intexit() {
    kill -SIGINT $PID
}

trap intexit INT

alembic -x dbname=sqlite:////sqlite/users.db upgrade head
python3 opentarock/server/__init__.py &
PID=$!

wait
