# '''use tornado as web server
# '''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application

import tornado.ioloop
import tornado.web
import tornado.wsgi

from tornado.options import options, define

define('port', type=int, default=8080)


class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello from tornado')


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    tornado_app = tornado.web.Application(
        handlers=[
            (r'/hello-tornado*', HelloHandler),
            (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ],
        static_path=os.path.join(os.path.dirname(__file__), 'static')
        )
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
