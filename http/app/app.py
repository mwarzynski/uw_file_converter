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

STATIC_DIR = "./static"

def term_handler(sig, frame):
    """ Handle SIGTERM signal from Docker """
    sys.exit(0)

class MainHandler(tornado.web.RequestHandler):
    """ Handler class for incoming HTTP requests """

    def get(self, *args, **kwargs):
        self.write("Hello, world")

class Application(tornado.web.Application):
    """ Main application controller """

    def __init__(self):
        self.mongo = motor.motor_tornado.MotorClient('db', 27017).convertdb

        handlers = [
            (r"/api/v1/auth/login", LoginHandler, dict(mongo=self.mongo)),
            (r"/api/v1/auth/logout", LogoutHandler, dict(mongo=self.mongo)),
            (r"/api/v1/upload/(.*)", UploadHandler, dict(mongo=self.mongo)),
            (r"/()$", tornado.web.StaticFileHandler, dict(path=os.path.join(STATIC_DIR,"index.html"))),
            (r"/(.*)", tornado.web.StaticFileHandler, dict(path=STATIC_DIR)),
        ]

        settings = {
            "cookie_secret": "4llY0urBa53Ar3B310ngT0U5"
        }
        super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    signal.signal(signal.SIGTERM, term_handler)

    try:
        app = Application()
        app.listen(5000)
        tornado.ioloop.IOLoop.current().start()
    finally:
        logging.info("Exiting...")
