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
    try:
        data = json.loads(message)
    except:
        LOG.error("invalid done message")
        return

    if data['user'] in live_web_sockets:
        ws = live_web_sockets[data['user']]
        if not ws.ws_connection or not ws.ws_connection.stream.socket:
            del live_web_sockets[data['user']]
        else:
            ws.write_message({
                'name': data['name'],
                'filetype': data['filetype'],
                'token': data['token'],
                'converted_at': data['converted_at']
            })

