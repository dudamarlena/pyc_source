# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/tests/test_service.py
# Compiled at: 2016-01-06 17:02:32
# Size of source mod 2**32: 1289 bytes
from wolverine.module.service import MicroService, ServiceMessage, ServiceDef
from wolverine.test import TestMicroApp

class TestService(object):

    def test_micro_service(event_loop):
        app = TestMicroApp(loop=event_loop)
        options = {'op_1': 'test', 'op_2': True}
        service = MicroService(app, name='test', version=2, **options)
        assert service.name == 'test'
        assert service.version == 2
        assert service.options['op_1'] == 'test'
        assert service.options['op_2']

    def test_service_message(self):
        message = ServiceMessage()
        message.data = [{'name': 'test', 'version': 1}]
        assert message.has_error() != True
        message.err({'exception': 'failed', 'severity': 'high'})
        assert message.has_error()
        assert message.response() == {'data': [{'name': 'test', 'version': 1}], 
         'errors': [{'exception': 'failed', 'severity': 'high'}]}

    def test_service_def(self):
        service = ServiceDef(name='test', version='2')
        service.routes.append('test/method')
        assert service.fqn() == 'wolverine:service/test/2'
        assert str(service) == str({'name': 'test', 
         'routes': ['test/method'], 
         'version': '2'})