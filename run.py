from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from create_blog import app
from ConfigParser import SafeConfigParser
import tornado.options
tornado.options.parse_command_line()

parser = SafeConfigParser()
parser.read('config.txt')
lport = parser.get('config', 'PORT')


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(lport)
print('Server running on http://localhost:' + lport)
try:
    IOLoop.instance().start()
except:
    print('\nExiting...')
    IOLoop.instance().stop()
