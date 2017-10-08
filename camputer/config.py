class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/dev.db'


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/test.db'

class TravisConfig(BaseConfig):
    """Travis CI configuration"""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/db/camputer.db'