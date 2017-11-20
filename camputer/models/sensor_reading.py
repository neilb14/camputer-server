from camputer import db

class SensorReading(db.Model):
    __tablename__ = 'sensor_reading'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Float)
    uom = db.Column(db.String)

    def __init__(self, name, timestamp=None, value=None, uom=None):
        self.name = name
        self.timestamp = timestamp
        self.value = value
        self.uom = uom

    def __repr__(self):
        return '<SensorReading %s %d %s at %s>' % (self.name, self.value, self.uom, self.timestamp)