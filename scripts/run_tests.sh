#!/usr/bin/env bash

mkdir -p .sqlite
py.test -rsx --color=yes --cov opentarock --cov-report \
    term-missing --cov-report html --cov-config .coveragerc --pep8 tests
