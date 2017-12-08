from collections import deque
from threading import Lock

from tornado.ioloop import PeriodicCallback
from tornado.websocket import WebSocketHandler

from .._native import ffi, lib


@ffi.callback("void(void *, SizedString)")
def callback(h, s):
    handler = ffi.from_handle(h)
    s = ffi.unpack(s.data, s.len).decode("utf-8")

    handler.queue.append(s)


class EchoHandler(WebSocketHandler):

    def open(self):
        print("Websocket opened")
        self.lock = Lock()
        self.queue = deque()
        self.pc = PeriodicCallback(self.sender, 10)
        self.pc.start()

    def on_message(self, message):
        data = message.encode("utf-8")
        self._handle = ffi.new_handle(self)
        lib.process(data, len(data), callback, self._handle)

    def on_close(self):
        print("Websocket closed")
        self.pc.stop()

    def sender(self):
        msg_count = len(self.queue)
        for _ in range(msg_count):
            msg = self.queue.popleft()
            self.write_message(msg)
