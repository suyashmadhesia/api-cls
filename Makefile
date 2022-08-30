setup-linux:
	python3 -m venv venv
	. ./venv/bin/activate
	pip install -r ./requirements.txt

setup-windows:
	python -m venv venv
	. ./venv/Scripts/activate
	pip install -r ./requirements.txt

.ONESHELL: setup-linux setup-windows

