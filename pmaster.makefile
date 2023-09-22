# --------==== Project Side ====--------
PROJECT = /active/pmaster
PROJECT_DATA = /dat/pmaster
AUX_LIB = /active/joption

all:
	echo "define your default task here"

install_pkg:
	pip install -r requirements.txt

dirs:
	mkdir -p $(PROJECT_DATA)
	
