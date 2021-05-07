#file -- merge_into_dw --
### Creates merged table from salesdb and swapi.dev api ###
### this isn't an api, kind of a misnomer ###

import psycopg2
import requests
import datetime
import swapi
import numpy as np
import pandas as pd
from faker import Faker
from faker.providers.internet import Provider
import re
from db_util import *



# create initial table
def create_dw_table():
	# database connection
	db_connect = connect_to_db()
	cur = db_connect.cursor()

	# create table
	try:
		table_creation = cur.execute("CREATE TABLE dw (id serial PRIMARY KEY, starship varchar, quantity smallint, price decimal, sales_rep varchar, promo_code varchar, film_title varchar, film_date varchar);")
	except:
		# delete rows if already created
		cur.execute("DELETE FROM dw;")

	db_connect.close()

# sql joins from salesdb and helper to create merged 'dw' table
# this could have been a View, since the addition of the helper table,
# ships_to_films, made it possible to do this without hitting any apis
# or performing trasnformations
def merge_dw_table():
	# database connection
	db_connect = connect_to_db()
	cur = db_connect.cursor()

	# SQL Join from salesdb and ships_to_films helper
	cur.execute("SELECT salesdb.poster_content, salesdb.quantity, salesdb.price, salesdb.sales_rep, salesdb.promo_code, ships_to_films.film_title, ships_to_films.film_date FROM salesdb INNER JOIN ships_to_films ON salesdb.poster_content = ships_to_films.starship;")
	rows = cur.fetchall()

	for i in range(len(rows)):
		row = rows[i]
		insert_row = cur.execute('''INSERT INTO dw ( starship, quantity,  price,  sales_rep,  promo_code, film_title, film_date) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

	# debug
	print("----------")
	print("dw db completed: " + str(datetime.datetime.now()))
	print("dw table output: ")
	cur.execute("SELECT COUNT(*) FROM dw;")
	print(cur.fetchone())
	cur.execute("SELECT * FROM dw limit 5;")
	print(cur.fetchall())

	db_connect.close()


