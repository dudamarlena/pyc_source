# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/queue.py
# Compiled at: 2016-06-11 06:32:43
import zmq
from .args import ArgumentParser
from .common import DEFAULT_REQ_PORT
from .common import DEFAULT_RES_PORT

def command():
    parser = ArgumentParser(description='jps queue', service=True, publisher=False, subscriber=False)
    args = parser.parse_args()
    main(args.request_port, args.response_port)


def main(req_port=DEFAULT_REQ_PORT, res_port=DEFAULT_RES_PORT):
    """main of queue

    :param req_port: port for clients
    :param res_port: port for servers
    """
    try:
        try:
            context = zmq.Context(1)
            frontend_service = context.socket(zmq.XREP)
            backend_service = context.socket(zmq.XREQ)
            frontend_service.bind(('tcp://*:{req_port}').format(req_port=req_port))
            backend_service.bind(('tcp://*:{res_port}').format(res_port=res_port))
            zmq.device(zmq.QUEUE, frontend_service, backend_service)
        except KeyboardInterrupt:
            pass

    finally:
        frontend_service.close()
        backend_service.close()
        context.term()


if __name__ == '__main__':
    main()