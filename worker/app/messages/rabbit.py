import pika
import logging

LOG = logging.getLogger('rabbit')
LOG.setLevel(logging.DEBUG)


class Rabbit:

    initialized_queues = set()

    connection = None
    channel = None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', retry_delay=1, connection_attempts=60))
        self.channel = self.connection.channel()

    def __del__(self):
        self.channel.close()
        self.connection.close()

    def queue_initialize(self, queue):
        if queue not in self.initialized_queues:
            self.channel.queue_declare(queue, auto_delete=False)
            self.initialized_queues.add(queue)

    def send(self, message, queue="to-convert"):
        self.queue_initialize(queue)
        self.channel.basic_publish(exchange="", routing_key=queue, body=message)

    def listen(self, callback, queue="to-convert"):
        self.queue_initialize(queue)
        for method_frame, properties, body in self.channel.consume(queue):
            # Do something with the data.
            try:
                callback(body)
            except Exception as e:
                LOG.error(e)

            # Notify that the message is acknowledged.
            self.channel.basic_ack(method_frame.delivery_tag)

        # Cancel the consumer and any pending messages.
        self.channel.cancel()
