import piko

class Messages:

    queue = "to-convert"

    connection = None
    channel = None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def __del__(self):
        self.connection.close()

    def send(self, message):
        self.channel.basic_publish(exchange="", routing_key=self.queue, body=message)


