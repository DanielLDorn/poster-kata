1# flask app

from flask import Flask, render_template
from db_util import *
import main
import os
import * from tests

# create database connection
db_connect = connect_to_db()
cur = db_connect.cursor()

app = Flask(__name__)


# made it here then run tests
if "TEST" in os.environ:
	if os.environ["TEST"] == "travis":
		test_salesdb()
		test_helper_table()
		test_helper_table()
		sys.exit(0)



@app.route('/')
def main_app():
	cur.execute("SELECT * FROM salesdb limit 25;")
	print(cur.fetchall())
	heading_salesdb = ['pizza', 'is', 'great']
	data_salesdb = [[1, 2, 3], [4, 5, 6]]
	
	return render_template('index.html', headings_salesdb=headings_salesdb, data_salesdb=data_salesdb)

if __name__ == '__main__':
	app.run(debug = True, host="0.0.0.0")