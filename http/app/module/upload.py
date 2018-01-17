""" File upload handling module """
import uuid
import tornado.web
import logging
import os

from .auth import (AuthBaseHandler, UnauthorizedError)

__UPLOAD__ = "/upload"

LOG = logging.getLogger("upload")
LOG.setLevel(logging.DEBUG)


def get_upload_token():
    return str(uuid.uuid4())


@tornado.web.stream_request_body
class UploadHandler(AuthBaseHandler):
    """ Handler for PUT upload requests """

    def __init__(self, *args, **kwargs):
        self.file = None
        self.filename = ""
        self.token = ""
        self.mongo = None

        super(UploadHandler, self).__init__(*args, **kwargs)

    def initialize(self, mongo):
        self.bytes_read = 0
        self.mongo = mongo

    async def prepare(self):
        if not self.current_user:
            raise UnauthorizedError()

        self.filename = self.request.headers.get("X-Filename", "")
        self.token = get_upload_token()
        path = os.path.join(__UPLOAD__, self.token)
        LOG.debug("Opening %s...", path)
        self.file = open(path, "wb")

    def put(self):
        self.mongo.uploaded.insert_one({
            'name': self.filename,
            'token': self.token,
            'user': self.current_user.decode('utf-8')
        })

        self.write({
            'name': self.filename,
            'token': self.token,
            'status': 'OK',
            'bytesReceived': self.bytes_read
        })

    def data_received(self, chunk):
        self.file.write(chunk)
        self.bytes_read += len(chunk)

    def on_finish(self):
        LOG.debug("Closing file...")
        if self.file:
            self.file.close()
            self.file = None

