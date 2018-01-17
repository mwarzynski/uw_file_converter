import pika
import logging
import threading

LOG = logging.getLogger('rabbit')
LOG.setLevel(logging.DEBUG)


def receive_messages(callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='done')

    channel.basic_consume(callback,
                          queue='done',
                          no_ack=True)
    mq_recieve_thread = threading.Thread(target=channel.start_consuming)
    mq_recieve_thread.start()

