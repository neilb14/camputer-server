from camputer import db

class Temperature(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    value = db.Column(db.Integer)

    def __init__(self, timestamp=None, value=None):
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        return '<Sample %d at %d>' % (self.value, self.timestamp)