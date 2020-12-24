# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/tests/common/test_async_eventlet.py
# Compiled at: 2019-08-30 19:22:58
# Size of source mod 2**32: 931 bytes
import logging, unittest, six
if six.PY3:
    from unittest import mock
else:
    import mock
from engineio.async_drivers import eventlet as async_eventlet

class TestAsyncEventlet(unittest.TestCase):

    def setUp(self):
        logging.getLogger('engineio').setLevel(logging.NOTSET)

    def test_bad_environ(self):
        wsgi = async_eventlet.WebSocketWSGI(None)
        environ = {'foo': 'bar'}
        start_response = 'bar'
        self.assertRaises(RuntimeError, wsgi, environ, start_response)

    @mock.patch('engineio.async_drivers.eventlet._WebSocketWSGI.__call__', return_value='data')
    def test_wsgi_call(self, _WebSocketWSGI):
        _WebSocketWSGI.__call__ = lambda e, s: 'data'
        environ = {'eventlet.input': mock.MagicMock()}
        start_response = 'bar'
        wsgi = async_eventlet.WebSocketWSGI(None)
        self.assertEqual(wsgi(environ, start_response), 'data')