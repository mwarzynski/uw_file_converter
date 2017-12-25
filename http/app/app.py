"""
Main module of HTTP Server
"""
import logging
import sys
import signal
import tornado.ioloop
import tornado.web

def term_handler():
    """ Handle SIGTERM signal from Docker """
    sys.exit(0)

class MainHandler(tornado.web.RequestHandler):
    """ Handler class for incoming HTTP requests """
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write("Hello, world")

def make_app():
    """ Build main app """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    log = logging.getLogger()
    log.setLevel("debug")
    signal.signal(signal.SIGTERM, term_handler)

    try:
        app = make_app()
        app.listen(5000)
        tornado.ioloop.IOLoop.current().start()
    finally:
        logging.info("Exiting...")
