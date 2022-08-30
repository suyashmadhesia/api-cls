## Requirements to run this project.
* Install [Python](https://www.python.org/downloads/)
* Install [pip](https://pip.pypa.io/en/stable/)
* Install [Postgres](https://www.postgresql.org/download/)
## General info
This is backend of classroom app written in Django rest framework.

## Local Database Setup (Postgresql)


Enter these command in psql terminal:
```
$ CREATE DATABASE djangodb;
$ CREATE USER django WITH ENCRYPTED PASSWORD '1234';
$ GRANT ALL PRIVILEGES ON DATABASE djangodb TO django;
```
	
## Setup
To run this project, install it locally:


For Linux User (Install Python, Pip and Postgres):
```
$ cd api-cls
$ make setup
$ ./migratedb
$ ./run-app
```

For windows user (Install Python, Pip and Postgres):
```
$ make setup
$ make run-migrations
$ python manage.py runserver
```
