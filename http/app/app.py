""" Main module of HTTP Server """
import logging
import os
import sys
import signal
import tornado.ioloop
import tornado.web
import motor.motor_tornado
from module.upload import UploadHandler
from module.download import DownloadHandler
from module.auth import (LoginHandler, LogoutHandler, RegisterHandler)
from module.convert import ConvertHandler
from module.files import FilesHandler
from module.delete import DeleteHandler, ConvertDeleteHandler
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
            (r"/api/v1/auth/register", RegisterHandler, dict(mongo=self.mongo)),
            (r"/api/v1/auth/login", LoginHandler, dict(mongo=self.mongo)),
            (r"/api/v1/auth/logout", LogoutHandler, dict(mongo=self.mongo)),
            (r"/api/v1/files", FilesHandler, dict(mongo=self.mongo)),
            (r"/api/v1/files/upload", UploadHandler, dict(mongo=self.mongo)),
            (r"/api/v1/files/download/(.*)", DownloadHandler, dict(mongo=self.mongo)),
            (r"/api/v1/files/delete/(.*)", DeleteHandler, dict(mongo=self.mongo)),
            (r"/api/v1/files/convert", ConvertHandler, dict(mongo=self.mongo,rabbit=self.writer)),
            (r"/api/v1/files/convert/delete/(.*)/(.*)", ConvertDeleteHandler, dict(mongo=self.mongo)),
            (r"/()$", XSRFStaticHandler,
             dict(path=os.path.join(STATIC_DIR, "index.html"))),
            (r"/(.*)", XSRFStaticHandler, dict(path=STATIC_DIR)),
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
