""" File deletion handling module """
import uuid
import tornado.web
import tornado.gen
import logging
import os
import json

from .auth import (AuthBaseHandler, UnauthorizedError)
from .upload import __UPLOAD__

LOG = logging.getLogger("delete")
LOG.setLevel(logging.DEBUG)


class DeleteHandler(AuthBaseHandler):
    """ Handler for POST convert requests """

    def __init__(self, *args, **kwargs):
        self.mongo = None

        super(DeleteHandler, self).__init__(*args, **kwargs)

    def initialize(self, mongo):
        self.mongo = mongo

    async def post(self, token):
        if not self.current_user:
            raise UnauthorizedError()

        file = await self.mongo.uploaded.find_one({
            'token': token,
            'user': self.current_user.decode('utf-8')
        })
        if not file:
            LOG.warning("There is no uploaded file for token: " + str(token))
            self.clear()
            self.set_status(404)
            return

        result = await self.mongo.uploaded.delete_one({
            'token': token,
            'user': self.current_user.decode('utf-8')
        })
        if not result:
            LOG.warning("Could not perform delete from mongo, token: " + str(token))
            self.clear()
            self.set_status(500)
            return

        path = os.path.join(__UPLOAD__, token)
        try:
            os.remove(path)
        except:
            pass

class ConvertDeleteHandler(AuthBaseHandler):
    """ Handler for POST convert requests """

    def __init__(self, *args, **kwargs):
        self.mongo = None

        super(DeleteHandler, self).__init__(*args, **kwargs)

    def initialize(self, mongo):
        self.mongo = mongo

    async def post(self, token):
        if not self.current_user:
            raise UnauthorizedError()

        result = await self.mongo.converts.find_one({
            'token': token,
            'user': self.current_user.decode('utf-8')
        })
        if not result:
            LOG.warning("There is no converted file for token: " + str(token))
            self.clear()
            self.set_status(404)
            return

        path = result['filepath']

        if not os.path.isfile(path):
            self.clear()
            self.set_status(404)
            return

        try:
            os.remove(path)
        except:
            pass

