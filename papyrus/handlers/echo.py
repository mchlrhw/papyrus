from tornado.websocket import WebSocketHandler

from .._native import ffi, lib


class EchoHandler(WebSocketHandler):

    def open(self):
        print("Websocket opened")

    def on_message(self, message):
        data = message.encode("utf-8")
        s = lib.process(data, len(data))
        s = ffi.unpack(s.data, s.len).decode("utf-8")
        self.write_message(s)

    def on_close(self):
        print("Websocket closed")
