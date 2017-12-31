from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from camputer import create_app, db

app = create_app('camputer.config.ProductionConfig')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()(venv)
