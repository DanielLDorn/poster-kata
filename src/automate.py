### generates fake data for 'salesdb' ###

import psycopg2
import requests
import swapi
import numpy as np
import pandas as pd
from faker import Faker
from faker.providers.internet import Provider

pd.set_option('display.max_columns', None)

fake = Faker()

### Columns for salesdb
# poster_content | string | "Millennium Falcon"
# quantity | int | 7						
# price | decimal | 2.9						
# email | string | "sally_skywalker@gmail.com"
# sales_rep | string | "tej@swposters.com"	
# promo_code | string | "radio"				

### TODO
# 4. Pull in other Data with API
# 6. Update SQL Database


### Generate the rows
def create_rows(number_of_rows, max_sales_per_order, max_price, number_of_employees):
	
	# add columns to DataFrame
	df = pd.DataFrame(columns=['poster_content', 'quantity', 'price', 'email', 'sales_rep', 'promo_code'])

	# add fake data to data frame
	df['poster_content'] = generate_poster_content(number_of_rows)
	df['quantity'] = np.random.randint(1, max_sales_per_order, number_of_rows)
	df['price'] = np.around(np.random.uniform(1.5, max_price, number_of_rows), decimals=2)
	df['email'] = generate_purchaser_emails(number_of_rows)
	df['sales_rep'] = generate_sales_rep(number_of_rows, number_of_employees)
	df['promo_code'] = generate_promo_codes(number_of_rows)

	return df

### Export the data
def export_sw_data(data_to_export):

	# create database connection
	db_connect = psycopg2.connect(
		host = "db",
		database = "postgres",
		user = "postgres",
		password = "postgres"
	)

	# psycopg2 won't autocommit
	# https://stackoverflow.com/questions/18068901/python-psycopg2-not-inserting-into-postgresql-table/18237335#18237335
	db_connect.autocommit = True

	# cursor
	cur = db_connect.cursor()

	# create table
	try:
		table_creation = cur.execute("CREATE TABLE salesdb (id serial PRIMARY KEY, poster_content varchar, quantity smallint, price decimal, email varchar, sales_rep varchar, promo_code varchar);")
	except:
		pass

	# delete previous commits
	try:
		cur.execute("DELETE FROM salesdb;")
	except:
		pass

	# insert new data
	for index, row in data_to_export.iterrows():
		insert_row = cur.execute("INSERT INTO salesdb (poster_content, quantity, price, email, sales_rep, promo_code) VALUES (%s, %s, %s, %s, %s, %s)", (row['poster_content'], row['quantity'], row['price'], row['email'], row['sales_rep'], row['promo_code']))

	# debug
	# print("salesdb table output: ")
	# print(cur.execute("SELECT COUNT(*) FROM salesdb;"))
	# print(cur.fetchall())

	db_connect.close()

### Generate Poster Content
def generate_poster_content(number_of_rows):
	posters_inventory = []

	# generate the posters that we carry
	endpoints = ["starships/", "planets/", "people/"]
	for endpoint in endpoints:
		# should this be wrapped in a try/except
		# can we trust this data source?
		response = requests.get(url="https://swapi.dev/api/" + endpoint)
		data = response.json()['results']
		for item in data:
			posters_inventory.append(item['name'])

	return np.random.choice(posters_inventory, number_of_rows)

### Generate Emails
def generate_purchaser_emails(number_of_rows):
	emails = []
	for i in range(0, number_of_rows):
		emails.append(fake.ascii_email())
	return emails

### Generate Sales Rep Emails
def generate_sales_rep(number_of_rows, number_of_employees):
	
	# generate random style for each employee, company loathes consistency
	email_styles = np.random.choice(["underscore", "dots", "initials"], number_of_employees)

	# generate employee emails
	sales_reps_emails = []
	for email_style in email_styles:
		if email_style == "underscore":
			sales_rep_email = fake.first_name().lower() + "_" + fake.last_name().lower() + "@swposters.com"
		elif email_style == "dots":
			sales_rep_email = fake.first_name().lower() + "." + fake.last_name().lower() + "@swposters.com"
		elif email_style == "initials":
			sales_rep_email = fake.first_name()[0].lower() + fake.first_name()[0].lower() + fake.last_name()[0].lower() + "@swposters.com"
		sales_reps_emails.append(sales_rep_email)

	# apply employee emails to all fields
	return np.random.choice(sales_reps_emails, number_of_rows)

### Generate Promo Codes Data
def generate_promo_codes(number_of_rows):
	promo_codes = ["tatooine", "luke", "princess_leia", "chewbacca", "scythe", "if_its_free_give_me_three", "march20"]
	return np.random.choice(promo_codes, number_of_rows)


### GENERATING DATA CALLS ###

# constants
max_sales_per_order = 100
max_price = 2500
number_of_employees = 12

# generate pandas data
created_sw_data = create_rows(1000, max_sales_per_order, max_price, number_of_employees)

# export data
exported_data = export_sw_data(created_sw_data)
