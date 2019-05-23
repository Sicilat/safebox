import sqlite3
import time
import datetime
import random

conn = sqlite3.connect('test.db')
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS testtable1(datestamp TEXT, keyword TEXT)')

def dynamic_data_entry(keyword):
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	value = random.randrange(0, 100)
	c.execute("INSERT INTO testtable1 (datestamp, keyword) VALUES (?, ?)", (date, keyword))
	conn.commit()

create_table()
well = str(input())
dynamic_data_entry(well)
sql = "SELECT * FROM testtable1 WHERE keyword='" + str(well) + "'"
print(sql)
c.execute(sql)
print(c.fetchall())


c.close()
conn.close()
