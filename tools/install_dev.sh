#!/usr/bin/env bash

cd "$(dirname "$0")/.."

if [[ -x /usr/bin/python3.6 ]] ; then
    PYTHON3=/usr/bin/python3.6
    sudo apt-get install python3.6-venv -y
else
if [[ -x /usr/bin/python3.5 ]] ; then
    PYTHON3=/usr/bin/python3.5
    sudo apt-get install python3.5-venv -y
else
    PYTHON3=/usr/bin/python3
    sudo apt-get install python3-venv -y
fi
fi

${PYTHON3} -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install .[dev]
