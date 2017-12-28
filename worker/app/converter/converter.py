import json
import logging
import time
from pymongo import MongoClient

LOG = logging.getLogger('converter')
LOG.setLevel(logging.DEBUG)

__UPLOAD__ = "/upload"


class Converter:

    def __init__(self, notifier):
        mongo_client = MongoClient('db', 27017)
        self.mongo = mongo_client.convertdb
        self.notifier = notifier

    def on_message(self, body):
        data = json.loads(body)

        try:
            token = data['token']
            input = __UPLOAD__ + "/" + token
            type_from = data['convert_from']
            type_to = data['convert_to']
            user = data['user']
        except KeyError as e:
            LOG.info("Invalid message key: " + str(e))
            return

        output = input + "." + str(type_to)

        message = {
            "user": user,
            "token": token,
            "file-input": input,
            "file-output": output
        }

        try:
            self.convert(type_from, type_to, input, output)
        except FileNotFoundError:
            LOG.info("Invalid token.")
            return
        except Exception as e:
            LOG.debug(e)
            message["status"] = "error"
            self.notify(message)
            return

        message["status"] = "done"
        self.notify(message)

    def convert(self, type_from, type_to, input, output):
        with open(input, 'rb') as f:
            data = f.read()

        # TODO: Convert the file accordingly to types.

        with open(output, 'wb') as f:
            f.write(data)

        pass

    def notify(self, message):
        message['converted_at'] = int(time.time())
        self.mongo.converts.update(
                { 'token': message["token"] },
                message,
                upsert=True
        )
        self.notifier.send(json.dumps(message))

