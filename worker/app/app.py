"""
Main module of Worker
"""
import logging
import sys
import signal
from converter import converter
from messages import rabbit

logging.basicConfig(filename='worker.log',level=logging.DEBUG)
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


def term_handler():
    """ Handle SIGTERM signal from Docker """
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, term_handler)

    try:
        rabbit = rabbit.Rabbit()

        converter = converter.Converter(rabbit)
        rabbit.listen(converter.on_message)
    finally:
        logging.info("Exiting...")
