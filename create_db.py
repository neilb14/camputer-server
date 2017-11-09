#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""
import os, sys, getopt
from datetime import datetime

from camputer import db, create_app
from camputer.models.sensor_reading import SensorReading

def main(argv):
    is_load = False
    config = 'camputer.config.DevelopmentConfig'
    help_message = 'create_db.py -l -c <config>\r\nconfig can be:\r\n   camputer.config.DevelopmentConfig (default)\r\n   camputer.config.TestingConfig\r\n   camputer.config.ProductionConfig'
    try:
        opts, args = getopt.getopt(argv,"hlc:",["config="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt == '-l':
            is_load = True
        elif opt in ("-c", "--config"):
            config = arg

    app = create_app(config)
    db.create_all()
    if is_load:
        load_sample_data()

def load_sample_data():
    t1 = SensorReading('temperature', datetime.utcnow(), 23)
    t2 = SensorReading('temperature', datetime.utcnow(), 15)
    t3 = SensorReading('temperature', datetime.utcnow(), 2)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.commit()

if __name__ == "__main__":
    main(sys.argv[1:])