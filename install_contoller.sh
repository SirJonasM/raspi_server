#!/bin/bash
set +x

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r .requirments_controller

