### Runs all steps to generate database and create merge ###
### Generates salesdb using functions in automate.py ###
### Creates merged table using functions in merge_table_api.py ###

import psycopg2
import requests
import swapi
import numpy as np
import pandas as pd
from faker import Faker
from faker.providers.internet import Provider
import datetime
from generate_salesdb import *
from merge_into_dw import *
from db_util import *


### Generate salesdb table ###

pd.set_option('display.max_columns', None)

# constants
max_sales_per_order = 100
max_price = 2500
number_of_employees = 18
rows_to_create = 1000

# generate pandas data
created_sw_data = create_rows(rows_to_create, max_sales_per_order, max_price, number_of_employees)

# export data
exported_data = export_sw_data(created_sw_data)



### Create 'dw' table from join of salesdb and ships_to_films ###

# create dw table
create_dw_table()

# merge and upload
merge_dw_table()