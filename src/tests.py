# simple unit tests to confirm setup

# create database connection
db_connect = connect_to_db()
cur = db_connect.cursor()


# confirm salesdb
def test_salesdb():
	cur.execute("SELECT COUNT(*) FROM salesdb;")
	number = cur.fetchone()[0]

	assert number == 1000, "`salesdb` not completed properly"


# test helper table
def test_helper_table():
	cur.execute("SELECT COUNT(*) FROM ships_to_films;")
	number = cur.fetchone()[0]

	assert number > 15 and number < 50 , "`helper_table` not completed properly"


# test 600 - 800 in dw
def test_helper_table():
	cur.execute("SELECT COUNT(*) FROM dw;")
	number = cur.fetchone()[0]

	assert number > 600 and number < 900 , "`dw` not completed properly"



