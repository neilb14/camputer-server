# camputer-server
[![Build Status](https://travis-ci.org/neilb14/camputer-server.svg?branch=master)](https://travis-ci.org/neilb14/camputer-server)

# Installation
After connecting the pi:
```bash
$ sudo apt-get update -y
$ sudo apt-get install python3-pip git
$ git clone https://github.com/neilb14/camputer-server.git
$ cd camputer-server
$ pip3 install -r requirements.txt
```

### Create and initialize the sqlite database:
```bash
$ $ sudo apt-get install sqlite3
$ sudo mkdir /var/db
$ sudo chown pi:pi /var/db
$ python3 create_db.py -l -c camputer.config.ProductionConfig
```
Omit the -l flag above to avoid adding dummy readings.

### Ensure that you can host the flask app:
```bash
$ python3 production.py runserver
```

And in another shell:
```bash
$ curl localhost:5000/sensorreadings/last?name=temperature
```
You should get a dummy sample that was loaded in the `create_db.py` script.

### Setup UWSGI
```bash
$ pip3 install uwsgi
$ ~/.local/bin/uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:application
```
And in another shell:
```bash
$ curl localhost:5000/sensorreadings/last?name=temperature
```
You should get a dummy sample that was loaded in the `create_db.py` script.

Now get it running on a socket:
```bash
$ sudo mkdir -p /var/www/camputer
$ sudo chown pi:www-data /var/www/camputer
$ ~/.local/bin/uwsgi -i camputer.ini
```
Then check that the socket file exists at: `/var/www/camputer/camputer.sock`.

Now configure UWSGI to start on boot:
`sudo vi /etc/rc.local` and add the following line before the exit:

```
/usr/local/bin/uwsgi --ini /home/pi/sampleApp/uwsgi_config.ini --uid www-data --gid www-data --daemonize /var/log/uwsgi.log
```

Then you should be able to start the service by running:
```bash
$ sudo systemctl start rc-local.service
```
Then ensure that the socket exists in: `/var/www/camputer`
And tail the log at: `/var/log/uwsgi.log` to see if there are any errors.
The output in the log should be similar to the output seen in the previous commands.

## Setup Nginx to host UWSGI app
```bash
$ sudo apt-get install nginx
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo vi /etc/nginx/sites-available/camputer
```
Edit the camputer site with the following:
```bash 
server {
 listen 80;
 server_name localhost;

 location /api { try_files $uri @app; }
 location @app {
   include uwsgi_params;
   uwsgi_pass unix:/var/www/camputer/camputer.sock;
 }
}
```
Then create a symbolic link in sites-enabled:
```bash
$ sudo ln -s /etc/nginx/sites-available/camputer  /etc/nginx/sites-enabled
```
And restart NGINX:
```bash
$ sudo service nginx restart
```

Finally test it out:
```bash
$ curl localhost/api/sensorreadings/last?name=temperature
```
# Enable sensors
Best to update the pi and firmware:

```bash
$ sudo apt-get upgrade
$ sudo apt-get install rpi-update
$ sudo rpi-update
```

## Enable the DS18B20 temperature sensor
[From the Adafruit DS18B20 Guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20)
Plug the temperature wire into GPIO4 (jumper 7)
```bash
$ sudo vi /boot/config.txt
```
Add the following at the bottom of that file:
```bash
dtoverlay=w1-gpio
```
Then reboot.

```bash
$ sudo modprobe w1-gpio
$ sudo modprobe w1-therm
$ cd /sys/bus/w1/devices
$ ls
$ cd 28-xxxx (change this to match what serial number pops up)
$ cat w1_slave
```
Should see a temperature reading.

Next run the python script (note, only runs with Python 2):
```bash
$ cd ~/camputer-server/scripts
$ python2 ds18b20.py
$ curl localhost/api/sensorreadings/last?name=outside 
```
And should see the sensor reading inserted into the database from the script.

## Enable the AM2302 temperature, humidity sensor
[Follow ModMyPi instructions](https://www.modmypi.com/blog/am2302-temphumidity-sensor) to install the Adafruit_Python_DHT libraries.

If you plug the sensor wire into GPIO17 (jumper 11) then no parameters are required to run the script:
```bash
$ cd ~/camputer-server/scripts/python2
$ python2 am2302.py
```
Should print a temperature and humidity reading. Also will write a record to the database. 
```bash
$ curl localhost/api/sensorreadings/last?name=temperature
$ curl localhost/api/sensorreadings/last?name=humidity
```
Should return readings from running the script previously.

## Darksky Weather
Script grabs the current weather from Darksky API:

```bash
$ python3 fetch_temperature.py -k DARKSKY_API_KEY -u http://localhost:8080
```

## Run scripts automatically through cron

crontab can look like:
```bash
*/5 * * * * python2 /home/pi/camputer-server/scripts/python2/ds18b20.py
*/5 * * * * python2 /home/pi/camputer-server/scripts/python2/am2302.py
*/15 * * * * python3 fetch_temperature.py -k DARKSKY_API_KEY -u http://localhost:8080
```

