"""
Main module of HTTP Server
"""
import logging
import sys
import signal
import tornado.ioloop
import tornado.web
from module.upload import (UploadHandler, UploadRequestHandler)

def term_handler():
    """ Handle SIGTERM signal from Docker """
    sys.exit(0)

class MainHandler(tornado.web.RequestHandler):
    """ Handler class for incoming HTTP requests """
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write("Hello, world")

class Application(tornado.web.Application):
    """ Main application controller """

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/upload/request", UploadRequestHandler),
            (r"/upload/(.*)", UploadHandler)
        ]
        super(Application, self).__init__(handlers)

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
