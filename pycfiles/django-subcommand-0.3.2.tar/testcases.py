# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ikeda/.virtualenvs/client-for-tastypie/tastypie-queryset-client/queryset_client/tests/testcases.py
# Compiled at: 2012-07-14 16:29:56
import sys, socket, threading
from StringIO import StringIO
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers import basehttp
from django.test.testcases import TransactionTestCase
from django.core.management import call_command
from queryset_client import Client
sys.stdout = StringIO()
sys.stderr = StringIO()

class StoppableWSGIServer(basehttp.WSGIServer):
    """WSGIServer with short timeout, so that server thread can stop this server."""

    def server_bind(self):
        """Sets timeout to 1 second."""
        basehttp.WSGIServer.server_bind(self)
        self.socket.settimeout(1)

    def get_request(self):
        """Checks for timeout when getting request."""
        try:
            sock, address = self.socket.accept()
            sock.settimeout(None)
            return (sock, address)
        except socket.timeout:
            raise

        return


class TestServerThread(threading.Thread):
    """Thread for running a http server while tests are running."""

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self._stopevent = threading.Event()
        self.started = threading.Event()
        self.error = None
        super(TestServerThread, self).__init__()
        return

    def run(self):
        """Sets up test server and database and loops over handling http requests."""
        try:
            handler = basehttp.AdminMediaHandler(WSGIHandler())
            server_address = (self.address, self.port)
            httpd = StoppableWSGIServer(server_address, basehttp.WSGIRequestHandler)
            httpd.set_app(handler)
            self.started.set()
        except basehttp.WSGIServerException as e:
            self.error = e
            self.started.set()
            return

        from django.conf import settings
        if settings.DATABASE_ENGINE == 'sqlite3' and (not settings.TEST_DATABASE_NAME or settings.TEST_DATABASE_NAME == ':memory:'):
            if hasattr(self, 'fixtures'):
                call_command('loaddata', *self.fixtures, **{'verbosity': 0})
        while not self._stopevent.isSet():
            httpd.handle_request()

    def join(self, timeout=None):
        """Stop the thread and wait for it to finish."""
        self._stopevent.set()
        threading.Thread.join(self, timeout)


class TestServerTestCase(TransactionTestCase):

    def start_test_server(self, address='127.0.0.1', port=8001):
        """Creates a live test server object (instance of WSGIServer)."""
        self.server_thread = TestServerThread(address, port)
        self.server_thread.start()
        self.server_thread.started.wait()
        if self.server_thread.error:
            raise self.server_thread.error

    def stop_test_server(self):
        if self.server_thread:
            self.server_thread.join()


def get_client(url='http://127.0.0.1:8001/base/v1/', auth=None, strict_field=True):
    return Client(url, auth=auth, strict_field=strict_field)