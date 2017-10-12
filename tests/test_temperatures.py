import json
from datetime import datetime, timedelta
from tests.base import BaseTestCase
from camputer import db
from camputer.models import Temperature

class TestTemperaturesService(BaseTestCase):
    """Tests for the Temperatures Service."""

    def add_temperature(self, timestamp=datetime.utcnow(), value=None): 
        db.session.add(Temperature(timestamp, value))

    def test_last_temperature_reading(self):
        self.add_temperature(datetime.utcnow() + timedelta(seconds=-2*60*60), 10)
        self.add_temperature(datetime.utcnow() + timedelta(seconds=-60*60), 20)
        self.add_temperature(datetime.utcnow(), 30)
        db.session.commit()
        """Ensure the /temperature/last route behaves correctly."""
        response = self.client.get('/temperatures/last')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(30, data['value'])
        self.assertIn('c', data['uom'])
