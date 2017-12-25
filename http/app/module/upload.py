""" File upload handling module """
import uuid
import tornado.web
import logging
import os

__UPLOAD__ = "/upload"

log = logging.getLogger("upload")
log.setLevel(logging.INFO)

def get_upload_token():
    return str(uuid.uuid4())

@tornado.web.stream_request_body
class UploadHandler(tornado.web.RequestHandler):
    """ Handler for PUT upload requests """

    @property
    def redis(self):
        return self.application.redis

    def initialize(self):
        self.bytes_read = 0
  
    def prepare(self):
        token = self.path_args[0]
        # Check if token is valid
        if True:
            path = os.path.join(__UPLOAD__, token)
            log.info("Opening %s..." % path)
            self.file = open(path, "wb")


    def put(self, token):
        log.info("PUT %s" % token)
        self.write({
            'status': 'OK',
            'bytesReceived': self.bytes_read
        })

    def data_received(self, chunk):
        self.file.write(chunk)
        self.bytes_read += len(chunk)

class UploadRequestHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(get_upload_token())
