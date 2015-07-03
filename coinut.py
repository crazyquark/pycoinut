#!/usr/bin/python

import sys, urllib, json, sqlite3
from filelock import FileLock

url = 'https://coinut.com/api/tick/BTCUSD'

conn = sqlite3.connect('coinut.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS ticker (timestamp integer, price real)''') 

conn.close()

prev_price = -1
while(True):
	try:
		lock = FileLock('coinut.lock')
		
		response = urllib.urlopen(url);
		data = json.loads(response.read())
	
		timestamp = long(data['timestamp'])
		price = float(data['tick'])
	
		if price != prev_price:
			if lock.acquire():
				conn = sqlite3.connect('coinut.db')
				c = conn.cursor()
			
				with conn:
					values = (timestamp, price,)
					c.execute("INSERT INTO ticker VALUES (?,?)", values)
	
					print values

					conn.commit()
					
					lock.release()
					
			prev_price = price
	except KeyboardInterrupt:
		print 'Exiting...'
		sys.exit(0)
	except:
		continue


