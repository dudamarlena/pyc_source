# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/master.py
# Compiled at: 2016-06-11 06:32:43
from multiprocessing import Process
import threading, os, signal
from .args import ArgumentParser
from . import forwarder
from . import queue
from .common import DEFAULT_PUB_PORT
from .common import DEFAULT_SUB_PORT
from .common import DEFAULT_REQ_PORT
from .common import DEFAULT_RES_PORT

def command():
    parser = ArgumentParser(description='jps master', service=True)
    args = parser.parse_args()
    main(args.request_port, args.response_port, args.publisher_port, args.subscriber_port)


def main(req_port=DEFAULT_REQ_PORT, res_port=DEFAULT_RES_PORT, pub_port=DEFAULT_PUB_PORT, sub_port=DEFAULT_SUB_PORT):
    p1 = Process(target=queue.main, args=(req_port, res_port))
    p1.start()
    forwarder.main(pub_port, sub_port)
    p1.join()