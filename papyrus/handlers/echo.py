from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from .._native import ffi, lib


@ffi.callback("void(void *, SizedString)")
def callback(h, s):
    handler = ffi.from_handle(h)
    s = ffi.unpack(s.data, s.len).decode("utf-8")

    loop = IOLoop.current()
    loop.spawn_callback(handler.write_message, s)


class EchoHandler(WebSocketHandler):

    def open(self):
        print("Websocket opened")
        self._handle = ffi.new_handle(self)

    def on_message(self, message):
        data = message.encode("utf-8")
        lib.process(data, len(data), callback, self._handle)

    def on_close(self):
        print("Websocket closed")
