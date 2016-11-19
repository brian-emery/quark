from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from create_blog import app
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.txt')
lport = parser.get('config', 'PORT')


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(lport)
IOLoop.instance().start()
