# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_handler_http.py
# Compiled at: 2015-04-13 10:14:07
import shutil, tempfile
from httmock import HTTMock
from dyntftpd.handlers.http import HTTPHandler
from . import TFTPServerTestCase

def get_small_file(url, request):
    return 'small file'


def bigger_than_max_size(url, request):
    return 'x' * 2000


def get_404(url, request):
    return {'status_code': 404, 
       'content': '404 error'}


class TestHTTPHandler(TFTPServerTestCase):

    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()
        return super(TestHTTPHandler, self).setUp(handler=HTTPHandler, handler_args={'http': {'cache_dir': self.cache_dir, 
                    'whitelist': [
                                'http://www.download.tld'], 
                    'maxsize': 1000}})

    def tearDown(self):
        try:
            shutil.rmtree(self.cache_dir)
        except OSError:
            pass

        super(TestHTTPHandler, self).tearDown()

    def test_retrieve_file(self):
        with HTTMock(get_small_file) as (mock):
            self.get_file('http://www.download.tld/superfile')
            data, _ = self.recv()
            self.assertEqual(data, '\x00\x03\x00\x01small file')
            self.ack_n(1)

    def test_404(self):
        with HTTMock(get_404) as (mock):
            self.get_file('http://www.download.tld/superfile')
            data, _ = self.recv()
            self.assertTrue(data.startswith('\x00\x05\x00\x02'))

    def test_maxsize(self):
        with HTTMock(bigger_than_max_size) as (mock):
            self.get_file('http://www.download.tld/superfile')
            data, _ = self.recv()
            self.assertTrue(data.startswith('\x00\x05\x00\x02'))

    def test_whitelist(self):
        """ If whitelist is not satisfied, no HTTP request is done.
        """
        self.get_file('http://www.forbidden.com/superfile')
        data, _ = self.recv()
        self.assertTrue(data.startswith('\x00\x05\x00\x02'))


class TestHTTPHandlerWithTimeout(TFTPServerTestCase):

    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()
        return super(TestHTTPHandlerWithTimeout, self).setUp(handler=HTTPHandler, handler_args={'http': {'cache_dir': self.cache_dir, 
                    'timeout': 0.001}})

    def tearDown(self):
        shutil.rmtree(self.cache_dir)
        super(TestHTTPHandlerWithTimeout, self).tearDown()

    def test_timeout(self):
        with HTTMock(get_small_file) as (mock):
            self.get_file('http://www.download.tld/superfile')
            data, _ = self.recv()
            self.assertTrue(data.startswith('\x00\x05\x00\x02'))