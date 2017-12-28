import pika


class Consumer:

    queue = "to-convert"

    connection = None
    channel = None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()

    def __del__(self):
        self.channel.close()
        self.connection.close()

    def run(self):
        for method_frame, properties, body in self.channel.consume(self.queue):
            # Do something.
            print(method_frame)
            print(properties)
            print(body)

            # Notify that the message is acknowledged.
            self.channel.basic_ack(method_frame.delivery_tag)

        # Cancel the consumer and any pending messages.
        self.channel.cancel()
