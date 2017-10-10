#!/usr/bin/python
import sys, getopt, sqlite3, Adafruit_DHT
from datetime import datetime

SQL_INSERT_TEMPERATURE = "INSERT INTO Temperatures (timestamp, value) VALUES (?,?)"

def main(argv):
	help_message = 'am2302.py -p <gpiopin> -d <dbfile>'
	dbfile = '/var/db/camputer.db'	
	gpiopin = 17
	try:
		opts, args = getopt.getopt(argv, "hp:d:", ["gpiopin=", "dbfile="])
	except getopt.GetoptError:
		print(help_message)
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print(help_message)
			sys.exit()
		elif opt in ("-p", "--gpiopin"):
			gpiopin = arg
		elif opt in ("-d", "--dbfile"):
			dbfile = arg
	
	humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		conn = sqlite3.connect(dbfile)
		c = conn.cursor()
		c.execute(SQL_INSERT_TEMPERATURE, (datetime.utcnow(), temperature))
		conn.commit()
		conn.close()
		
if __name__ == "__main__":
	main(sys.argv[1:])
