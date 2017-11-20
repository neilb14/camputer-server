import json
from datetime import datetime, timedelta
from tests.base import BaseTestCase
from camputer import db
from camputer.models.sensor_reading import SensorReading

class TestSensorReadingService(BaseTestCase):
    """Tests for the Sensor Reading Service."""

    def add_sensor_reading(self, timestamp=datetime.utcnow(), value=None): 
        db.session.add(SensorReading('temperature', timestamp, value, 'f'))

    def test_last_temperature_reading(self):
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-2*60*60), 10)
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-60*60), 20)
        self.add_sensor_reading(datetime.utcnow(), 30)
        db.session.commit()
        """Ensure the /temperature/last route behaves correctly."""
        response = self.client.get('/sensorreadings/last?name=temperature')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(30, data['value'])
        self.assertIn('f', data['uom'])

    def test_temperature_range(self):
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-5*60*60), 10)
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-4*60*60), 12)
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-3*60*60), 14)
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-2*60*60), 16)
        self.add_sensor_reading(datetime.utcnow() + timedelta(seconds=-60*60), 18)
        self.add_sensor_reading(datetime.utcnow(), 20)
        db.session.commit()
        response = self.client.get('/sensorreadings?name=temperature&hours=3')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, data['count'])
        self.assertEqual(3, len(data['readings']))
        self.assertEqual(20, data['readings'][0]['value'])

    def test_add_temperature_sensor_reading(self):
        timestamp = datetime.utcnow()
        response = self.client.post('/sensorreadings',
                                    data=json.dumps(dict(
                                            name= 'temperature',
                                            timestamp= timestamp.isoformat(),
                                            value=12.3,
                                            uom= 'f'
                                    )),
                                    content_type='application/json'
                                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual('success', data['status'])
        reading = SensorReading.query\
                        .filter(SensorReading.timestamp == timestamp)\
                        .filter(SensorReading.name == 'temperature')\
                        .first()
        self.assertIsNotNone(reading)
        self.assertEqual(12.3, reading.value)
        self.assertEqual('f', reading.uom)

    def test_add_any_sensor_reading(self):
        timestamp = datetime.utcnow()
        response = self.client.post('/sensorreadings',
                                    data=json.dumps(dict(
                                            name= 'blow at high dough',
                                            timestamp= timestamp.isoformat(),
                                            value=12.3,
                                            uom= '%'
                                    )),
                                    content_type='application/json'
                                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual('success', data['status'])
        reading = SensorReading.query\
                        .filter(SensorReading.timestamp == timestamp)\
                        .filter(SensorReading.name == 'blow at high dough')\
                        .first()
        self.assertIsNotNone(reading)
        self.assertEqual(12.3, reading.value)
        self.assertEqual('%', reading.uom)

