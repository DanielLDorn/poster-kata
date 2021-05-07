#file -- generate_salesdb --
### generates fake data for 'salesdb' ###

import psycopg2
import requests
import swapi
import numpy as np
import pandas as pd
from faker import Faker
from faker.providers.internet import Provider
import datetime
from db_util import *

### Generate the rows
def create_rows(number_of_rows, max_sales_per_order, max_price, number_of_employees):
	
	fake = Faker()

	# add columns to DataFrame
	df = pd.DataFrame(columns=['poster_content', 'quantity', 'price', 'email', 'sales_rep', 'promo_code'])

	# add fake data to data frame
	df['poster_content'] = generate_poster_content(number_of_rows)
	df['quantity'] = np.random.randint(1, max_sales_per_order, number_of_rows)
	df['price'] = np.around(np.random.uniform(1.5, max_price, number_of_rows), decimals=2)
	df['email'] = [fake.ascii_email() for _ in range(number_of_rows)]
	df['sales_rep'] = generate_sales_rep(number_of_rows, number_of_employees)
	df['promo_code'] = generate_promo_codes(number_of_rows)

	return df

### Export the data
def export_sw_data(data_to_export):

	# create database connection
	db_connect = connect_to_db()
	cur = db_connect.cursor()

	# create table
	try:
		table_creation = cur.execute("CREATE TABLE salesdb (id serial PRIMARY KEY, poster_content varchar, quantity smallint, price decimal, email varchar, sales_rep varchar, promo_code varchar);")
	except:
		# delete rows if already created
		cur.execute("DELETE FROM salesdb;")

	# insert new data
	for index, row in data_to_export.iterrows():
		insert_row = cur.execute("INSERT INTO salesdb (poster_content, quantity, price, email, sales_rep, promo_code) VALUES (%s, %s, %s, %s, %s, %s)", (row['poster_content'], row['quantity'], row['price'], row['email'], row['sales_rep'], row['promo_code']))

	# debug
	print("----------")
	print("sales db completed: " + str(datetime.datetime.now()))
	print("salesdb table output: ")
	cur.execute("SELECT COUNT(*) FROM salesdb;")
	print(cur.fetchone())
	cur.execute("SELECT * FROM salesdb limit 5;")
	print(cur.fetchall())

	db_connect.close()

### Generate Poster Content
def generate_poster_content(number_of_rows):
	posters_inventory = []

	# generate the posters that we carry
	endpoints = ["starships/", "planets/", "people/"]
	for endpoint in endpoints:
		# should this be wrapped in a try/except
		response = requests.get(url="https://swapi.dev/api/" + endpoint)
		data = response.json()['results']
		for item in data:
			posters_inventory.append(item['name'])

	return np.random.choice(posters_inventory, number_of_rows)

### Generate Sales Rep Emails
def generate_sales_rep(number_of_rows, number_of_employees):
	fake = Faker()
	
	# generate random style for each employee, company loathes consistency
	sales_reps_emails = np.random.choice([
		fake.first_name().lower() + "_" + fake.last_name().lower() + "@swposters.com", # underscore
		fake.first_name().lower() + "." + fake.last_name().lower() + "@swposters.com", # dots
		fake.first_name()[0].lower() + fake.first_name()[0].lower() + fake.last_name()[0].lower() + "@swposters.com" # initials
		], number_of_employees)

	# apply employee emails to all fields
	return np.random.choice(sales_reps_emails, number_of_rows)

### Generate Promo Codes Data
def generate_promo_codes(number_of_rows):
	promo_codes = ["tatooine", "luke", "princess_leia", "chewbacca", "scythe", "if_its_free_give_me_three", "march20"]
	return np.random.choice(promo_codes, number_of_rows)
