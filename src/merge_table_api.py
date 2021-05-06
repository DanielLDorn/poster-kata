### Creates merged table from salesdb and swapi.dev api ###

import psycopg2
import requests
import swapi
import numpy as np
import pandas as pd
from faker import Faker
from faker.providers.internet import Provider
import re


# grab the unique
def get_unique_spaceships(db_connect):

	# cursor
	cur = db_connect.cursor()

	# create table -> are returned as tuples
	cur.execute("SELECT DISTINCT poster_content FROM salesdb;")
	unique_spaceships = cur.fetchall()

	return unique_spaceships

def get_movies_for_each_spaceship(unique_spaceships):
	spaceship_movies = {}
	
	for spaceship in unique_spaceships:
		spaceship = spaceship[0]
		if spaceship not in spaceship_movies:
			# use requests to search by name of starship and get number
			response = requests.get(url="https://swapi.dev/api/starships/", params={"search": spaceship})
			data = response.json()['results']

			if len(data) > 0:
				spaceship_movies[spaceship] = []

				# add films -> url endpoint -> http://swapi.dev/api/films/1/
				film_urls = data[0]['films']

				for film_url in film_urls:
					film = requests.get(url=film_url).json()
					spaceship_movies[spaceship].append({'film_title': film['title'], 'film_date': film['release_date']})

	return spaceship_movies


# combine and upload sales
def combine_and_upload(spaceship_movies, db_connect):

	# cursor
	cur = db_connect.cursor()

	# create table
	try:
		table_creation = cur.execute("CREATE TABLE mw (id serial PRIMARY KEY, poster_content varchar, film_title varchar, film_date varchar, quantity smallint, price decimal, sales_rep varchar, promo_code varchar);")
	except:
		pass

	# delete previous commits
	try:
		cur.execute("DELETE FROM mw;")
	except:
		pass

	# grab all sales, exclude 
	cur.execute("SELECT poster_content, quantity, price, sales_rep, promo_code FROM salesdb")
	sales = cur.fetchall()

	# insert new data
	for i in range(len(sales)):
		sale = sales[i]
		if sale[0] in spaceship_movies:
			for movie in spaceship_movies[sale[0]]:
				insert_row = cur.execute('''INSERT INTO mw (
												poster_content,
												film_title,
												film_date, 
												quantity, 
												price, 
												sales_rep, 
												promo_code
											) VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
											(
												sale[0], 
												movie['film_title'],
												movie['film_date'],
												sale[1], 
												sale[2], 
												sale[3], 
												sale[4]
											)
										)

	# debug
	# cur.execute("SELECT COUNT(*) FROM mw")
	# cur.execute("SELECT * FROM mw LIMIT 10;")
	# print(cur.fetchall())

### Merge Tables

# Open Database Connection
db_connect = psycopg2.connect(
	host = "db",
	database = "postgres",
	user = "postgres",
	password = "postgres"
)
db_connect.autocommit = True


# Grab Unique spaceships
unique_spaceships = get_unique_spaceships(db_connect)

# Grab the movies associated with each spaceship
movies_w_spaceships = get_movies_for_each_spaceship(unique_spaceships)

# # create a row for each sale w/ new movie data
rows = combine_and_upload(movies_w_spaceships, db_connect)


# Close Database Connection
db_connect.close()