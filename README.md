# Installation guide:
``` bash
git clone git@github.com:SirJonasM/raspi_server.github
cd raspi_server
git submodule init
git submodule update
pip install -r requirements.txt
python generate_makefiles.py
python run_make_files.py
python app.py
```


