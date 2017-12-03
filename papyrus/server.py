import tornado.web

from .routes import routes


def make_app():
    return tornado.web.Application(routes)
