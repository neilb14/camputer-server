#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""
import os
from datetime import datetime, timedelta

from camputer import db, create_app
from camputer.models import Temperature

app = create_app('camputer.config.DevelopmentConfig')

print(os.getcwd())
print(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()
temperature = Temperature(100, 23)
temperature2 = Temperature(101, 15)

db.session.add(temperature)
db.session.add(temperature2)

db.session.commit()