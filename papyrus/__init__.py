import tornado.ioloop

from .server import make_app


def run():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
