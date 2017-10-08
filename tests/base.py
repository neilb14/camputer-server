from flask_testing import TestCase
from camputer import create_app, db

class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('camputer.config.TestingConfig')

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()