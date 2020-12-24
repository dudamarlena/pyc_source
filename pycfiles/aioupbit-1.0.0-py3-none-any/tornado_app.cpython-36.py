# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aiounittest_tornado\tornado_app.py
# Compiled at: 2019-11-07 22:03:59
# Size of source mod 2**32: 1723 bytes
__doc__ = '\n\n只是简单的利用了aiounitest和学习了tornado本身的测试的代码\n'
import asyncio
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.testing import bind_unused_port, AsyncHTTPTestCase
from aiounittest import AsyncTestCase

class AsyncHTTPTest(AsyncTestCase):
    """AsyncHTTPTest"""

    def setUp(self):
        sock, port = bind_unused_port()
        self._AsyncHTTPTest__port = port
        self.app = self.get_app()
        self.http_server = HTTPServer((self.app), **self.get_httpserver_options())
        self.http_server.add_sockets([sock])

    def get_httpserver_options(self):
        return {}

    def tearDown(self):
        self.http_server.stop()
        self.http_server.stop()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.http_server.close_all_connections())
        del self.http_server
        del self.app
        super(AsyncHTTPTest, self).tearDown()

    def get_app(self):
        raise Exception('需要载入tornado 中的应用')

    def get_url(self, path: str) -> str:
        """Returns an absolute url for the given path on the test server."""
        return '%s://127.0.0.1:%s%s' % (self.get_protocol(), self.get_http_port(), path)

    def get_protocol(self) -> str:
        return 'http'

    def get_http_port(self) -> int:
        """Returns the port used by the server.

        A new port is chosen for each test.
        """
        return self._AsyncHTTPTest__port

    def get_http_client(self) -> AsyncHTTPClient:
        return AsyncHTTPClient()

    def get_event_loop(self):
        return asyncio.get_event_loop()