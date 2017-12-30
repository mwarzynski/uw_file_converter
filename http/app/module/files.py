""" File upload handling module """
import uuid
import tornado.web
import logging
import os
import json

from .auth import (AuthBaseHandler, UnauthorizedError)

LOG = logging.getLogger("files")
LOG.setLevel(logging.DEBUG)


class FilesHandler(AuthBaseHandler):
    """ Handler for GET download requests """

    def __init__(self, *args, **kwargs):
        self.mongo = None

        super(FilesHandler, self).__init__(*args, **kwargs)

    def initialize(self, mongo):
        self.mongo = mongo

    async def get(self):
        if not self.current_user:
            raise UnauthorizedError()

        files = []

        converted = False
        try:
            if int(self.get_argument('converted', 0)) > 0:
                converted = True
        except:
            pass

        if converted:
            async for file in self.mongo.converts.find({
                'user': self.current_user.decode('utf-8')
                }):
                files.append({
                    'token': file['token'],
                    'name': file['name'],
                    'type': file['filetype'],
                    'status': file['status']
                })
        else:
            async for file in self.mongo.uploaded.find({
                'user': self.current_user.decode('utf-8')
                }):
                files.append({
                    'token': file['token'],
                    'name': file['name'],
                })
            collection = self.mongo.converts

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            'files': files,
        }))

