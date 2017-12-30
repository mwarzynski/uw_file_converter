""" File upload handling module """
import uuid
import tornado.web
import logging
import os

from .auth import (AuthBaseHandler, UnauthorizedError)

__UPLOAD__ = "/upload"

LOG = logging.getLogger("upload")
LOG.setLevel(logging.DEBUG)


class DownloadHandler(AuthBaseHandler):
    """ Handler for GET download requests """

    def __init__(self, *args, **kwargs):
        self.mongo = None

        super(DownloadHandler, self).__init__(*args, **kwargs)

    def initialize(self, mongo):
        self.mongo = mongo

    async def get(self, token):
        if not self.current_user:
            raise UnauthorizedError()

        result = await self.mongo.converts.find_one({
            'token': token,
            'user': self.current_user.decode('utf-8')
        })
        if not result:
            LOG.warning("File for token (" + str(token) + ") not found.")
            self.clear()
            self.set_status(404)
            return

        path = result["filepath"]

        if not os.path.isfile(path):
            self.clear()
            self.set_status(404)
            return

        LOG.debug("Opening %s...", path)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + result['token'] + '.' + result['filetype'])

        with open(path, 'rb') as f:
            data = f.read()
            self.write(data)
        self.finish()

