#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""samples.py: Generate 3 hours of temperture data for testing."""
import os, sys, getopt, random, sqlite3
from os.path import dirname
sys.path.append(os.path.join(dirname(__file__), os.pardir))

from datetime import datetime, timedelta
from camputer import db, create_app
from camputer.models.sensor_reading import SensorReading

def create_readings(name, start, dev):
    value = random.gauss(start, dev)
    timestamp = datetime.utcnow() - timedelta(hours=3)
    while(timestamp <= datetime.utcnow()):
        t = SensorReading(name,timestamp, value, 'c')
        db.session.add(t)
        timestamp = timestamp + timedelta(minutes=5)
        value = random.gauss(value, dev)
    db.session.commit()

def main(argv):
    random.seed()
    config = 'camputer.config.DevelopmentConfig'
    help_message = 'temperatures_3hrs.py -c <config>\r\nconfig can be:\r\n   camputer.config.DevelopmentConfig (default)\r\n   camputer.config.TestingConfig\r\n   camputer.config.ProductionConfig'
    try:
        opts, args = getopt.getopt(argv,"hc:",["config="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-c", "--config"):
            config = arg
    
    app = create_app(config)
    create_readings('temperature',16,2)
    create_readings('outside',0,4)
    create_readings('darksky',0,4)
    

if __name__ == "__main__":
    main(sys.argv[1:])



