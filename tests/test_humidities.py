import json
from datetime import datetime
from tests.base import BaseTestCase
from camputer import db
from camputer.models import Humidity

class TestHumidityService(BaseTestCase):
    """Tests for the Humidity Service."""

    def test_last_humidity_reading(self):
        h1 = Humidity(datetime.utcnow(), 41.6)
        h2 = Humidity(datetime.utcnow(), 47.9)
        h3 = Humidity(datetime.utcnow(), 43.8)
        db.session.add(h1)
        db.session.add(h2)
        db.session.add(h3)
        db.session.commit()
        """Ensure the /humidity/last route behaves correctly."""
        response = self.client.get('/humidities/last')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(43.8, data['value'])
        self.assertIn('%', data['uom'])