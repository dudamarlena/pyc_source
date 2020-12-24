# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/forwarder.py
# Compiled at: 2016-06-11 06:32:43
import zmq
from .args import ArgumentParser
from .env import get_pub_port
from .env import get_sub_port

def command():
    parser = ArgumentParser(description='jps forwarder')
    args = parser.parse_args()
    main(args.publisher_port, args.subscriber_port)


def main(pub_port=None, sub_port=None):
    """main of forwarder

    :param sub_port: port for subscribers
    :param pub_port: port for publishers
    """
    try:
        try:
            if sub_port is None:
                sub_port = get_sub_port()
            if pub_port is None:
                pub_port = get_pub_port()
            context = zmq.Context(1)
            frontend = context.socket(zmq.SUB)
            backend = context.socket(zmq.PUB)
            frontend.bind(('tcp://*:{pub_port}').format(pub_port=pub_port))
            frontend.setsockopt(zmq.SUBSCRIBE, '')
            backend.bind(('tcp://*:{sub_port}').format(sub_port=sub_port))
            zmq.device(zmq.FORWARDER, frontend, backend)
        except KeyboardInterrupt:
            pass

    finally:
        frontend.close()
        backend.close()
        context.term()

    return


if __name__ == '__main__':
    main()