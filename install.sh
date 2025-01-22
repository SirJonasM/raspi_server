#!/bin/bash
set +x

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirments.txt
python3 generate_make_files.py
python3 run_make_files.py
cd rust
./build.sh
