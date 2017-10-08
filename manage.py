import unittest
from flask_script import Manager
from camputer import create_app, db

app = create_app('camputer.config.DevelopmentConfig')
manager = Manager(app)

@manager.command
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1    

if __name__ == '__main__':
    manager.run()