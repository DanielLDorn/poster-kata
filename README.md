# poster-kata

## About

[![Build Status](https://api.travis-ci.com/DanielLDorn/poster-kata.svg?branch=master&status=created)](https://travis-ci.com/github/DanielLDorn/poster-kata)

:star::ship:	Starships are the bomb.	:rocket::rocket::rocket:

This is a demo ETL exercise that generates a table called `salesdb`, hits an API https://swapi.dev/, and merges the table with the api data to create the table `dw`. The database and python code in this demo are deployed in a docker container using travis-ci.

## Tech Stack
- Containers:		Docker
- Language:			Python
- Database:			Postgres
- Web Framework:	Flask
- CI:				Travis-CI
- Hosting:			???

## Code Structure

./src/db_util.py -> connects to database
./src/main.py -> calls functions to create tables and data
./src/generate_salesdb.py -> functions that create `salesdb` table, hit swapi api, and create helper table
./src/merge_into_dw.py -> functions that create merged table
./src/flask_app.py -> generates the flask app
