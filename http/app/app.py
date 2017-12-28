""" Main module of HTTP Server """
import logging
import os
import sys
import signal
import tornado.ioloop
import tornado.web
import motor.motor_tornado
from module.upload import UploadHandler
from module.auth import (LoginHandler, LogoutHandler)
from module.convert import ConvertHandler
from messages.writer import Writer

STATIC_DIR = "./static"

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


def term_handler(sig, frame):
    """ Handle SIGTERM signal from Docker """
    sys.exit(0)


class XSRFStaticHandler(tornado.web.StaticFileHandler):
    def prepare(self):
        self.xsrf_token


class Application(tornado.web.Application):
    """ Main application controller """

    def __init__(self):
        self.writer = Writer()
        self.mongo = motor.motor_tornado.MotorClient('db', 27017).convertdb

        handlers = [
            (r"/api/v1/auth/login", LoginHandler, dict(mongo=self.mongo)),
            (r"/api/v1/auth/logout", LogoutHandler, dict(mongo=self.mongo)),
            (r"/api/v1/upload", UploadHandler, dict(mongo=self.mongo)),
            (r"/api/v1/convert", ConvertHandler, dict(mongo=self.mongo,rabbit=self.writer)),
            (r"/()$", XSRFStaticHandler,
             dict(path=os.path.join(STATIC_DIR, "index.html"))),
            (r"/static/(.*)", XSRFStaticHandler, dict(path=STATIC_DIR)),
        ]

        settings = {
            "cookie_secret": "4llY0urBa53Ar3B310ngT0U5",
            "xsrf_cookies": True
        }
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, term_handler)

    try:
        # Intitialize HTTP server.
        app = Application()
        app.listen(5000)
        tornado.ioloop.IOLoop.current().start()
    finally:
        logging.info("Exiting...")
