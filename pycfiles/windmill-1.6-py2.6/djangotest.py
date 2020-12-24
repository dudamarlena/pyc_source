# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/authoring/djangotest.py
# Compiled at: 2011-01-13 01:48:00
import socket, threading
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers import basehttp
from django.test.testcases import call_command
try:
    from django.test.testcases import TransactionTestCase as TestCase
except ImportError:
    from django.test.testcases import TestCase

class StoppableWSGIServer(basehttp.WSGIServer):
    """WSGIServer with short timeout, so that server thread can stop this server."""

    def server_bind(self):
        """Sets timeout to 1 second."""
        basehttp.WSGIServer.server_bind(self)
        self.socket.settimeout(1)

    def get_request(self):
        """Checks for timeout when getting request."""
        try:
            (sock, address) = self.socket.accept()
            sock.settimeout(None)
            return (sock, address)
        except socket.timeout:
            raise

        return


class TestServerThread(threading.Thread):
    """Thread for running a http server while tests are running."""

    def __init__(self, address, port, fixtures):
        self.address = address
        self.port = port
        self._stopevent = threading.Event()
        self.started = threading.Event()
        self.error = None
        self.fixtures = fixtures
        super(TestServerThread, self).__init__()
        return

    def run(self):
        """Sets up test server and database and loops over handling http requests."""
        try:
            handler = basehttp.AdminMediaHandler(WSGIHandler())
            httpd = None
            while httpd is None:
                try:
                    server_address = (
                     self.address, self.port)
                    httpd = StoppableWSGIServer(server_address, basehttp.WSGIRequestHandler)
                except basehttp.WSGIServerException, e:
                    if 'Address already in use' in str(e):
                        self.port += 1
                    else:
                        raise e

            httpd.set_app(handler)
            self.started.set()
        except basehttp.WSGIServerException, e:
            self.error = e
            self.started.set()
            return
        else:
            from django.conf import settings
            create_db = False
            if hasattr(settings, 'DATABASES'):
                if settings.DATABASES and (settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3' or settings.DATABASES['default']['TEST_NAME']):
                    create_db = True
            elif settings.DATABASE_ENGINE:
                if settings.DATABASE_ENGINE == 'sqlite3' and (not settings.TEST_DATABASE_NAME or settings.TEST_DATABASE_NAME == ':memory:'):
                    create_db = True
            if create_db:
                from django.db import connection
                db_name = connection.creation.create_test_db(0)
                if hasattr(self, 'fixtures'):
                    call_command('loaddata', *self.fixtures, **{'verbosity': 1})
            while not self._stopevent.isSet():
                httpd.handle_request()

        httpd.server_close()
        return

    def join(self, timeout=None):
        """Stop the thread and wait for it to finish."""
        self._stopevent.set()
        threading.Thread.join(self, timeout)


def start_test_server(self, address='127.0.0.1', port=8000, fixtures=[]):
    """Creates a live test server object (instance of WSGIServer)."""
    self.server_thread = TestServerThread(address, port, fixtures=fixtures)
    self.server_thread.start()
    self.server_thread.started.wait()
    if self.server_thread.error:
        raise self.server_thread.error


start_test_server.__test__ = False

def stop_test_server(self):
    if self.server_thread:
        self.server_thread.join()


stop_test_server.__test__ = False
TestCase.start_test_server = classmethod(start_test_server)
TestCase.stop_test_server = classmethod(stop_test_server)
from windmill.authoring import unit

class WindmillDjangoUnitTest(TestCase, unit.WindmillUnitTestCase):
    test_port = 8000
    fixtures = []

    def setUp(self):
        self.start_test_server('127.0.0.1', self.test_port, self.fixtures)
        self.test_url = 'http://127.0.0.1:%d' % self.server_thread.port
        unit.WindmillUnitTestCase.setUp(self)

    def tearDown(self):
        unit.WindmillUnitTestCase.tearDown(self)
        self.stop_test_server()


WindmillDjangoTransactionUnitTest = WindmillDjangoUnitTest