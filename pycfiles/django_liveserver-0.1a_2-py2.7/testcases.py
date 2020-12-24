# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/django_liveserver/testcases.py
# Compiled at: 2012-03-03 13:32:37
import os, sys, threading, select, socket, errno
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer, WSGIServerException
from django.views.static import serve
from django.test.testcases import TransactionTestCase

class _ImprovedEvent(threading._Event):
    """
    Does the same as `threading.Event` except it overrides the wait() method
    with some code borrowed from Python 2.7 to return the set state of the
    event (see: http://hg.python.org/cpython/rev/b5aa8aa78c0f/). This allows
    to know whether the wait() method exited normally or because of the
    timeout. This class can be removed when Django supports only Python >= 2.7.
    """

    def wait(self, timeout=None):
        self._Event__cond.acquire()
        try:
            if not self._Event__flag:
                self._Event__cond.wait(timeout)
            return self._Event__flag
        finally:
            self._Event__cond.release()


class QuietWSGIRequestHandler(WSGIRequestHandler):
    """
    Just a regular WSGIRequestHandler except it doesn't log to the standard
    output any of the requests received, so as to not clutter the output for
    the tests' results.
    """

    def log_message(*args):
        pass


class StoppableWSGIServer(WSGIServer):
    """
    The code in this class is borrowed from the `SocketServer.BaseServer` class
    in Python 2.6. The important functionality here is that the server is non-
    blocking and that it can be shut down at any moment. This is made possible
    by the server regularly polling the socket and checking if it has been
    asked to stop.
    Note for the future: Once Django stops supporting Python 2.6, this class
    can be removed as `WSGIServer` will have this ability to shutdown on
    demand and will not require the use of the _ImprovedEvent class whose code
    is borrowed from Python 2.7.
    """

    def __init__(self, *args, **kwargs):
        WSGIServer.__init__(self, *args, **kwargs)
        self.__is_shut_down = _ImprovedEvent()
        self.__serving = False

    def serve_forever(self, poll_interval=0.5):
        """
        Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds.
        """
        self.__serving = True
        self.__is_shut_down.clear()
        while self.__serving:
            r, w, e = select.select([self], [], [], poll_interval)
            if r:
                self._handle_request_noblock()

        self.__is_shut_down.set()

    def shutdown(self):
        """
        Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.__serving = False
        if not self.__is_shut_down.wait(2):
            raise RuntimeError('Failed to shutdown the live test server in 2 seconds. The server might be stuck or generating a slow response.')

    def handle_request(self):
        """Handle one request, possibly blocking.
        """
        fd_sets = select.select([self], [], [], None)
        if not fd_sets[0]:
            return
        else:
            self._handle_request_noblock()
            return

    def _handle_request_noblock(self):
        """
        Handle one request, without blocking.

        I assume that select.select has returned that the socket is
        readable before this function was called, so there should be
        no risk of blocking in get_request().
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return

        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except Exception:
                self.handle_error(request, client_address)
                self.close_request(request)


class _MediaFilesHandler(StaticFilesHandler):
    """
    Handler for serving the media files. This is a private class that is
    meant to be used solely as a convenience by LiveServerThread.
    """

    def get_base_dir(self):
        return settings.MEDIA_ROOT

    def get_base_url(self):
        return settings.MEDIA_URL

    def serve(self, request):
        return serve(request, self.file_path(request.path), document_root=self.get_base_dir())


class LiveServerThread(threading.Thread):
    """
    Thread for running a live http server while the tests are running.
    """

    def __init__(self, host, possible_ports, connections_override=None):
        self.host = host
        self.port = None
        self.possible_ports = possible_ports
        self.is_ready = threading.Event()
        self.error = None
        self.connections_override = connections_override
        super(LiveServerThread, self).__init__()
        return

    def run(self):
        """
        Sets up the live server and databases, and then loops over handling
        http requests.
        """
        if self.connections_override:
            from django.db import connections
            for alias, conn in self.connections_override.items():
                conn.allow_thread_sharing = True
                connections._connections[alias] = conn

        try:
            handler = StaticFilesHandler(_MediaFilesHandler(WSGIHandler()))
            for index, port in enumerate(self.possible_ports):
                try:
                    self.httpd = StoppableWSGIServer((
                     self.host, port), QuietWSGIRequestHandler)
                except WSGIServerException as e:
                    if sys.version_info < (2, 6):
                        error_code = e.args[0].args[0]
                    else:
                        error_code = e.args[0].errno
                    if index + 1 < len(self.possible_ports) and error_code == errno.EADDRINUSE:
                        continue
                    else:
                        raise
                else:
                    self.port = port
                    break

            self.httpd.set_app(handler)
            self.is_ready.set()
            self.httpd.serve_forever()
        except Exception as e:
            self.error = e
            self.is_ready.set()

    def join(self, timeout=None):
        if hasattr(self, 'httpd'):
            self.httpd.shutdown()
            self.httpd.server_close()
        super(LiveServerThread, self).join(timeout)


class LiveServerTestCase(TransactionTestCase):
    """
    Does basically the same as TransactionTestCase but also launches a live
    http server in a separate thread so that the tests may use another testing
    framework, such as Selenium for example, instead of the built-in dummy
    client.
    Note that it inherits from TransactionTestCase instead of TestCase because
    the threads do not share the same transactions (unless if using in-memory
    sqlite) and each thread needs to commit all their transactions so that the
    other thread can see the changes.
    """

    @property
    def live_server_url(self):
        return 'http://%s:%s' % (
         self.server_thread.host, self.server_thread.port)

    @classmethod
    def setUpClass(cls):
        connections_override = {}
        for conn in connections.all():
            if conn.settings_dict['ENGINE'] == 'django.db.backends.sqlite3' and conn.settings_dict['NAME'] == ':memory:':
                conn.allow_thread_sharing = True
                connections_override[conn.alias] = conn

        specified_address = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8081')
        possible_ports = []
        try:
            host, port_ranges = specified_address.split(':')
            for port_range in port_ranges.split(','):
                extremes = map(int, port_range.split('-'))
                assert len(extremes) in (1, 2)
                if len(extremes) == 1:
                    possible_ports.append(extremes[0])
                else:
                    for port in range(extremes[0], extremes[1] + 1):
                        possible_ports.append(port)

        except Exception:
            raise ImproperlyConfigured('Invalid address ("%s") for live server.' % specified_address)

        cls.server_thread = LiveServerThread(host, possible_ports, connections_override)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        cls.server_thread.is_ready.wait()
        if cls.server_thread.error:
            raise cls.server_thread.error
        super(LiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'server_thread'):
            cls.server_thread.join()
        super(LiveServerTestCase, cls).tearDownClass()