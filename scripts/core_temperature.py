#!/usr/bin/python
import os, re, sys, getopt, sqlite3
from datetime import datetime

SQL_INSERT_TEMPERATURE = "INSERT INTO sensor_reading (name, timestamp, value, uom) VALUES ('core', ?,?,'c')"

def main(argv):
	help_message = 'core_temperature.py -d <dbfile>'
	dbfile = '/var/db/camputer.db'
	try:
		opts, args = getopt.getopt(argv, "hd:", ["dbfile="])
	except getopt.GetoptError:
		print(help_message)
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print(help_message)
			sys.exit()
		elif opt in ("-d", "--dbfile"):
			dbfile = arg

	#result = os.popen("vcgencmd measure_temp").readline()
	result = "temp=21.3'C"
	coreTemp = None
	if result is not None and result != "":
	    coreTemp = float(re.sub("\'C", "", re.sub("^temp=", "", result)))
	if coreTemp is not None:
		print('CoreTemp={0:0.1f}*'.format(coreTemp))
		conn = sqlite3.connect(dbfile)
		c = conn.cursor()
		c.execute(SQL_INSERT_TEMPERATURE, (datetime.utcnow(), coreTemp))
		conn.commit()
		conn.close()

if __name__ == "__main__":
	main(sys.argv[1:])
