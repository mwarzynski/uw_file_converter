import logging
import json

import tornado.gen
import tornado.websocket

from .auth import AuthBaseHandler, UnauthorizedError

LOG = logging.getLogger('websocket')
LOG.setLevel(logging.DEBUG)


live_web_sockets = {}

class NotifierWebSocket(tornado.websocket.WebSocketHandler, AuthBaseHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        if not self.current_user:
            raise UnauthorizedError()
        live_web_sockets[self.current_user.decode('utf-8')] = self

    def on_close(self):
        if not self.current_user:
            raise UnauthorizedError()
        del live_web_sockets[self.current_user.decode('utf-8')]

    def on_message(self, message):
        pass


def callback(ch, method, properties, message):
    LOG.debug(message)
    return
    for ws in live_web_sockets:
        if not ws.ws_connection or not ws.ws_connection.stream.socket:
            removable.add(ws)
        else:
            ws.write_message(message)
    for ws in removable:
        live_web_sockets.remove(ws)

