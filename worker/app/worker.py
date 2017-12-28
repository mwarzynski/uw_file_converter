"""
Main module of Worker
"""
import logging
import sys
import signal
import consumer

def term_handler():
    """ Handle SIGTERM signal from Docker """
    sys.exit(0)


class Worker:
    """ Main  """

    consumer = None

    def __init__(self, consumer):
        self.consumer = consumer

    def start(self):
        self.consumer.run()


if __name__ == "__main__":
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    signal.signal(signal.SIGTERM, term_handler)

    try:
        consumer = consumer.Consumer()
        worker = Worker(consumer)
        worker.start()
    finally:
        logging.info("Exiting...")
