import json
import logging

LOG = logging.getLogger('converter')
LOG.setLevel(logging.DEBUG)

__UPLOAD__ = "/upload"


class Converter:

    def __init__(self, notifier):
        self.notifier = notifier

    def on_message(self, body):
        data = json.loads(body)

        try:
            input = __UPLOAD__ + "/" + data['token']
            type_from = data['convert_from']
            type_to = data['convert_to']
            user = data['user']
        except KeyError as e:
            LOG.info("Invalid message key: " + str(e))
            return

        output = input + "." + str(type_to)

        try:
            self.convert(type_from, type_to, input, output)
        except FileNotFoundError:
            LOG.info("Invalid token.")
            return
        except Exception as e:
            LOG.debug(e)
            self.notify(user, input, "", "error")
            return

        self.notify(user, input, output, "done")

    def convert(self, type_from, type_to, input, output):
        with open(input, 'rb') as f:
            data = f.read()

        # TODO: Convert the file accordingly to types.

        with open(output, 'wb') as f:
            f.write(data)

        pass

    def notify(self, user, input, output, status):
        message = {
            "user": user,
            "file": input,
            "file-output": output,
            "status": status
        }
        self.notifier.send(json.dumps(message))

