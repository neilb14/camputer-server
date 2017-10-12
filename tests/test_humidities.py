import json
from datetime import datetime, timedelta
from tests.base import BaseTestCase
from camputer import db
from camputer.models import Humidity

class TestHumidityService(BaseTestCase):
    """Tests for the Humidity Service."""

    def add_humidity(self, timestamp=datetime.utcnow(), value=None):
        db.session.add(Humidity(timestamp, value))

    def test_last_humidity_reading(self):
        self.add_humidity(datetime.utcnow()+timedelta(seconds=-2*60*60), 41.6)
        self.add_humidity(datetime.utcnow()+timedelta(seconds=-60*60), 47.9)
        self.add_humidity(datetime.utcnow(), 43.8)
        db.session.commit()
        """Ensure the /humidity/last route behaves correctly."""
        response = self.client.get('/humidities/last')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(43.8, data['value'])
        self.assertIn('%', data['uom'])