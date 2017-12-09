#!/home/neilb/camputer-server/venv/bin/python
from flup.server.fcgi import WSGIServer
from camputer import create_app

if __name__ == '__main__':
    WSGIServer(create_app('camputer.config.ProductionConfig')).run()
