import sys, os, glob, sqlite3, time
from datetime import datetime
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

SQL_INSERT_TEMPERATURE = "INSERT INTO sensor_reading (name, timestamp, value, uom) VALUES ('outside', ?,?,'c')"

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string)/1000.0
		return temp_c

def main(argv):
	dbfile = '/var/db/camputer.db'
	reading = read_temp()
	print('Temp={0:0.1f}*'.format(reading))
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute(SQL_INSERT_TEMPERATURE, (datetime.utcnow(), reading))
	conn.commit()
	conn.close()

if __name__ == "__main__":
	main(sys.argv[1:])
