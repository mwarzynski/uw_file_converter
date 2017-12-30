""" File upload handling module """
import uuid
import tornado.web
import tornado.gen
import logging
import os
import json

from .auth import (AuthBaseHandler, UnauthorizedError)
from .upload import __UPLOAD__

LOG = logging.getLogger("convert")
LOG.setLevel(logging.DEBUG)


class ConvertHandler(AuthBaseHandler):
    """ Handler for POST convert requests """

    def __init__(self, *args, **kwargs):
        self.file = None
        self.mongo = None
        self.rabbit = None

        super(ConvertHandler, self).__init__(*args, **kwargs)

    def prepare(self):
        if self.request.headers["Content-Type"].startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def initialize(self, mongo, rabbit):
        self.mongo = mongo
        self.rabbit = rabbit

    async def post(self):
        if not self.current_user:
            raise UnauthorizedError()

        try:
            token = self.json_args['token']
            convert_from = self.json_args['convert_from']
            convert_to = self.json_args['convert_to']
        except ValueError:
            self.clear()
            self.set_status(400)
            return

        file = await self.mongo.uploaded.find_one({
            'token': token,
            'user': self.current_user.decode('utf-8')
        })
        if not file:
            LOG.warning("There is no uploaded file for token: " + str(token))
            self.clear()
            self.set_status(404)
            return

        path = os.path.join(__UPLOAD__, token)

        message = {
            'convert_from': convert_from,
            'convert_to': convert_to,
            'token': token,
            'name': file['name'],
            'user': self.current_user.decode('utf-8')
        }
        self.rabbit.send(json.dumps(message))

