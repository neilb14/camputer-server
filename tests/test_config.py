import unittest
from flask import current_app
from flask_testing import TestCase
from camputer import create_app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return create_app('camputer.config.DevelopmentConfig')

    def test_app_is_development(self):
        self.assertFalse(current_app is None)
        self.assertTrue(current_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db/dev.db')
        self.assertTrue(current_app.config['DEBUG'] is True)


class TestTestingConfig(TestCase):
    def create_app(self):
        return create_app('camputer.config.TestingConfig')

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db/test.db')
        self.assertTrue(current_app.config['DEBUG'])
        self.assertTrue(current_app.config['TESTING'])

class TestProductionConfig(TestCase):
    def create_app(self):
        return create_app('camputer.config.ProductionConfig')

    def test_app_is_production(self):
        self.assertTrue(current_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////var/db/camputer.db')
        self.assertFalse(current_app.config['DEBUG'])
        self.assertFalse(current_app.config['TESTING'])

if __name__ == '__main__':
    unittest.main()