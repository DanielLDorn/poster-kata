#file -- merge_into_mw --
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


# grab the unique
def get_unique_spaceships():

	# database connection
	db_connect = connect_to_db()
	cur = db_connect.cursor()

	# create table -> are returned as tuples
	cur.execute("SELECT DISTINCT poster_content FROM salesdb;")
	unique_spaceships = cur.fetchall()

	db_connect.close()

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
def combine_and_upload(spaceship_movies):

	# database connection
	db_connect = connect_to_db()
	cur = db_connect.cursor()

	# create table
	try:
		table_creation = cur.execute("CREATE TABLE mw (id serial PRIMARY KEY, poster_content varchar, film_title varchar, film_date varchar, quantity smallint, price decimal, sales_rep varchar, promo_code varchar);")
	except:
		# delete rows if already created
		cur.execute("DELETE FROM mw;")

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
	print("----------")
	print("mw db completed: " + str(datetime.datetime.now()))
	print("mw table output: ")
	cur.execute("SELECT COUNT(*) FROM mw;")
	print(cur.fetchone())
	cur.execute("SELECT * FROM mw limit 5;")
	print(cur.fetchall())

	db_connect.close()
