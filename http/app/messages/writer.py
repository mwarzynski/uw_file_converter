import pika


class Writer:

    queue = "to-convert"

    connection = None
    channel = None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', retry_delay=1, connection_attempts=60))
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue, auto_delete=False)

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def send(self, message):
        self.channel.basic_publish(exchange="", routing_key=self.queue, body=message)
