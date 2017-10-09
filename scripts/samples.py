#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""samples.py: Generate dummy data for testing."""
import sys, getopt, random, sqlite3
sys.path.append('.')
from datetime import datetime
from camputer import db, create_app
from camputer.models import Temperature

def main(argv):
    random.seed()
    config = 'camputer.config.DevelopmentConfig'
    help_message = 'samples.py -c <config>\r\nconfig can be:\r\n   camputer.config.DevelopmentConfig (default)\r\n   camputer.config.TestingConfig\r\n   camputer.config.ProductionConfig'
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

    id = int(datetime.utcnow().strftime('%Y%m%d%H%M%S'))
    value = int((0.5 - random.random())*100)

    t = Temperature(datetime.utcnow(), value)
    db.session.add(t)
    db.session.commit()

if __name__ == "__main__":
    main(sys.argv[1:])



