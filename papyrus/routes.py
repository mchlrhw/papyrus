from tornado.web import url

from .handlers import EchoHandler


routes = [
    url(r"/echo", EchoHandler),
]
