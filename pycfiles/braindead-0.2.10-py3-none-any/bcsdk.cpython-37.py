# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/bcsdk/bcsdk.py
# Compiled at: 2019-12-09 06:47:00
# Size of source mod 2**32: 929 bytes
import logging, socketio, flask, requests, os
from bcsdk.impl.impl import _start_server, sio, _stop_server

class Handler:
    """Handler"""

    def __init__(self):
        global sio
        self.sio = sio

    def on_init(self, conf: dict):
        raise NotImplementedError()

    def on_destroy(self):
        raise NotImplementedError()

    def on_message(self, msg: dict):
        raise NotImplementedError()

    def send_message(self, msg: dict):
        sio.emit('response', msg)


def run_sdk(handler: Handler):
    _start_server(handler)


def stop_sdk():
    _stop_server()


def main():
    print('Starting SDK')
    from bcsdk.examples.mathoperations import MathOperationsHandler
    run_sdk(MathOperationsHandler())


if __name__ == '__main__':
    main()