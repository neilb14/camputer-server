#!/home/pi/camputer-server/venv/bin/python
from flup.server.fcgi import WSGIServer
from camputer import app

if __name__ == '__main__':
    WSGIServer(app).run()