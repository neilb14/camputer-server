from camputer import db

class SensorReading(db.Model):
    __tablename__ = 'sensor_reading'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Float)

    def __init__(self, name, timestamp=None, value=None):
        self.name = name
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        return '<SensorReading %s %d at %s>' % (self.name, self.value, self.timestamp)