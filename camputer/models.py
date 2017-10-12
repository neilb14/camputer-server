from camputer import db

class Temperature(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Integer)

    def __init__(self, timestamp=None, value=None):
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        return '<Temperature %d at %s>' % (self.value, self.timestamp)


class Humidity(db.Model):
    __tablename__ = 'humidities'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Float)

    def __init__(self, timestamp=None, value=None):
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        return '<Humidity %d at %s>' % (self.value, self.timestamp)