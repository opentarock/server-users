#!/usr/bin/env bash

py.test -rsx --color=yes --cov opentarock --cov-report \
    term-missing --cov-report html --cov-config .coveragerc --pep8 tests
