deps-linux:
ifneq ($(wildcard venv),)
	@echo "Found virtual environment..."
else
	@echo "Did not find virtual environment, creating..."
	python3 -m venv venv
endif
	@echo "Installing dependencies..."
	. ./venv/bin/activate
	pip install -r ./requirements.txt

deps-windows:
ifneq ($(wildcard venv),)
	@echo "Found virtual environment..."
else
	@echo "Did not find virtual environment, creating......"
	python -m venv venv
endif
	. .\venv\Scripts\activate
	@echo "Installing dependencies"
	pip install -r ./requirements.txt


UNAME := $(shell uname)
setup:
ifeq ($(UNAME), Windows)
	@echo "Windows detected...."
	make deps-windows
	@echo "To run this backend use 'make runapp' command in cmd. Make sure Database is setup and running..."
else
	@echo "Linux detected...."
	make deps-linux
	@echo "Giving permission to run scripts"
	sudo chmod +x ./run-app ./migratedb
	@echo "To run this backend use './run-app' command in terminal. Make sure Database is setup and running..."
endif


runapp:
	@echo "Running application..."
ifeq ($(UNAME), Windows)
	. .\venv\Scripts\activate
	python manage.py runserver
else
	. ./venv/bin/activate
	python3 manage.py runserver
endif

run-migrations:
		@echo "Running Migrations..."
ifeq ($(UNAME), Windows)
	. .\venv\Scripts\activate
	python manage.py makemigrations
	python manage.py migrate
else
	. ./venv/bin/activate
	python3 manage.py makemigrations
	python3 manage.py migrate
endif
	

.ONESHELL: setup deps-linux deps-windows runapp run-migrations

