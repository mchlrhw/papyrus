from tornado.websocket import WebSocketHandler

from .._native import ffi, lib


@ffi.callback("void(void *, SizedString)")
def callback(h, s):
    handler = ffi.from_handle(h)
    s = ffi.unpack(s.data, s.len).decode("utf-8")
    handler.write_message(s)


class EchoHandler(WebSocketHandler):

    def open(self):
        print("Websocket opened")

    def on_message(self, message):
        data = message.encode("utf-8")
        self._handle = ffi.new_handle(self)
        lib.process(data, len(data), callback, self._handle)

    def on_close(self):
        print("Websocket closed")
