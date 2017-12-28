import pika


class Writer:

    queue = "done"

    connection = None
    channel = None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def send(self, message):
        self.channel.basic_publish(exchange="", routing_key=self.queue, body=message)
