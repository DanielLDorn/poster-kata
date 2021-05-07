#file -- db_util --
### utility to connect to postgres database
### returns a connection with psycopg2
### still need to call .cursor() method to use

import psycopg2

def connect_to_db():
	# Open Database Connection
	db_connect = psycopg2.connect(
		host = "db",
		database = "postgres",
		user = "postgres",
		password = "postgres"
	)
	db_connect.autocommit = True

	return db_connect

