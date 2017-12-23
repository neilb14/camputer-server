#!/home/neilb/camputer-server/venv/bin/python
from camputer import create_app
application = create_app('camputer.config.ProductionConfig')
