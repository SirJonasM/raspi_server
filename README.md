# Prerequisits:
rust needs to be installed on a raspberry Pi only install the minimum package.

# Installation guide:
``` bash
git clone git@github.com:SirJonasM/raspi_server.github
cd raspi_server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_make_files.py
python run_make_files.py
cd rust
WINDOWS:
.\\build.bat
LINUX:
./build.sh
```
# Running the server:
```
python app.py
```
