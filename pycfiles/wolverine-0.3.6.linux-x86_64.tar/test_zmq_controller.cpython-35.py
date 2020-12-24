# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/tests/test_zmq_controller.py
# Compiled at: 2016-01-06 19:20:52
# Size of source mod 2**32: 1830 bytes
import socket, asyncio
from wolverine.module.controller.zmq import ZMQMicroController
from wolverine.module.service import ServiceMessage, MicroService
from wolverine.test import TestMicroApp

def test_zmq_controller(event_loop):
    app = TestMicroApp(loop=event_loop)
    ctrl = ZMQMicroController()
    app.register_module(ctrl)
    app.run()
    event_loop.run_until_complete(app.stop('SIGTERM'))


def test_zmq_controller_client(event_loop):
    app = TestMicroApp(loop=event_loop)
    ctrl = ZMQMicroController()
    options = {'address': 'tcp://' + socket.gethostbyname(socket.gethostname()), 
     'port': 1333, 
     'tags': ['version:1']}

    @ctrl.client('test', async=True, **options)
    def client_handler():
        yield from asyncio.sleep(1)
        print('client bound')

    app.register_module(ctrl)
    tasks = []

    @asyncio.coroutine
    def run_for(seconds):
        yield from asyncio.sleep(seconds)

    app.run()
    event_loop.run_until_complete(run_for(2))
    event_loop.run_until_complete(app.stop('SIGINT'))


def test_zmq_controller_service(event_loop):
    app = TestMicroApp(loop=event_loop)
    ctrl = ZMQMicroController()
    service = TestService(app)
    ctrl.register_service(service)
    app.register_module(ctrl)
    assert len(ctrl.services) == 1
    app.run()


class TestService(MicroService):

    def __init__(self, app, **options):
        self.delay = options.pop('delay', 1)
        self.routing = options.pop('routing', False)
        super(TestService, self).__init__(app, 'test', **options)

    def version(self, data):
        yield from asyncio.sleep(self.delay)
        return 1

    def ping(self, data):
        yield from asyncio.sleep(self.delay)
        response = ServiceMessage()
        response.data = data
        return response