import json
from datetime import datetime
from tests.base import BaseTestCase
from camputer import db
from camputer.models import Temperature

class TestTemperaturesService(BaseTestCase):
    """Tests for the Temperatures Service."""

    def test_last_temperature_reading(self):
        t1 = Temperature(datetime.utcnow(), 10)
        t2 = Temperature(datetime.utcnow(), 20)
        t3 = Temperature(datetime.utcnow(), 30)
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)
        db.session.commit()
        """Ensure the /temperature/last route behaves correctly."""
        response = self.client.get('/temperatures/last')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(30, data['value'])
        self.assertIn('c', data['uom'])