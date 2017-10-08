from sqlalchemy import Column, Integer, String
from camputer.database import Base

class Temperature(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    value = Column(Integer)

    def __init__(self, timestamp=None, value=None):
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        return '<Sample %d at %d>' % (self.value, self.timestamp)