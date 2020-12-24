# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/pyro_runner.py
# Compiled at: 2009-10-07 18:08:46
"""Run tests in multiple processes, communicating with Pyro"""
from __future__ import generators
import os

def iter_queue(queue, sentinel, **kwargs):
    """
    Iterate over a Queue.Queue instance until a sentinel is reached
    Will pass any extra keyword arguments to queue.get

    Created by Jimmy Retzlaff
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252498
    """
    while True:
        try:
            result = queue.get(**kwargs)
        except TypeError:
            result = queue.get()

        if result == sentinel:
            return
        yield result


from baserunner import BaseRunner

class PyroRunner(BaseRunner):
    __module__ = __name__
    SLEEP_INTERVAL_BETWEEN_RETRYING_CONNECTION = 0.5
    GET_TIMEOUT = 20

    def __init__(self, max_processes):
        BaseRunner.__init__(self)
        from Queue import Queue
        self.queue = Queue()
        self.max_processes = max_processes
        self.fixture_ids = {}
        self._parent_pid = os.getpid()
        self.num_fixtures = 0

    def _pyro_name(self, basename):
        """Return the name mangled for use in Testoob's RPC"""
        return ':testoob:%s:%s' % (basename, self._parent_pid)

    def _pyroloc_uri(self, basename):
        """Return the PYROLOC URI for the object, with proper mangling"""
        return 'PYROLOC://localhost/%s' % self._pyro_name(basename)

    def _get_pyro_proxy(self, basename, timeout=40):
        """Safely try to get a proxy to the object, looping until timing out"""
        import time, Pyro.core, Pyro.errors
        uri = self._pyroloc_uri(basename)
        starttime = time.time()
        while time.time() - starttime <= timeout:
            try:
                return Pyro.core.getProxyForURI(uri).getProxy()
            except Pyro.errors.ProtocolError:
                time.sleep(PyroRunner.SLEEP_INTERVAL_BETWEEN_RETRYING_CONNECTION)

        raise RuntimeError('getting the proxy has timed out')

    def _get_id(self):
        try:
            self.current_id += 1
        except AttributeError:
            self.current_id = 0

        return '%s.%s' % (self._parent_pid, self.current_id)

    def run(self, fixture):
        self._register_fixture(fixture, self._get_id())

    def _register_fixture(self, fixture, id):
        assert id not in self.fixture_ids
        self.fixture_ids[id] = fixture
        self.queue.put(id)
        self.num_fixtures += 1

    def _spawn_processes(self):
        if os.fork() != 0:
            return
        for i in xrange(1, self._num_processes()):
            if os.fork() == 0:
                self._client_code()

        self._client_code()

    def _num_processes(self):
        """Don't spawn more processes than there are fixtures"""
        return min(self.max_processes, self.num_fixtures)

    def done(self):
        for i in xrange(self._num_processes()):
            self.queue.put(None)

        self._spawn_processes()
        self._server_code()
        BaseRunner.done(self)
        return

    def _pyro_queue(self):
        import Pyro.core
        result = Pyro.core.ObjBase()
        result.delegateTo(self.queue)
        return result

    def _pyro_reporter(self):
        import Pyro.core
        result = Pyro.core.SynchronizedObjBase()
        result.delegateTo(self.reporter)
        return result

    def _server_code(self):
        """The Pyro server code, runs in the parent"""
        import Pyro.core, Pyro
        Pyro.config.PYRO_MOBILE_CODE = True
        Pyro.core.initServer(banner=False)
        daemon = Pyro.core.Daemon(host='localhost')
        daemon.connect(self._pyro_queue(), self._pyro_name('queue'))
        daemon.connect(self._pyro_reporter(), self._pyro_name('reporter'))
        daemon.requestLoop(condition=lambda : not self.queue.empty())
        daemon.shutdown()

    def _run_fixtures(self):
        queue = self._get_pyro_proxy('queue')
        remote_reporter = self._get_pyro_proxy('reporter')
        from testoob.reporting.reporter_proxy import ReporterProxy
        local_reporter = ReporterProxy()
        local_reporter.add_observer(remote_reporter)
        for id in iter_queue(queue, None, timeout=PyroRunner.GET_TIMEOUT):
            fixture = self.fixture_ids[id]
            fixture(local_reporter)

        return

    def _client_code(self):
        """The Pyro client code, runs in the child"""
        import Pyro.errors, Pyro.core, Pyro
        Pyro.config.PYRO_MOBILE_CODE = True
        Pyro.core.initClient(banner=False)
        import sys
        try:
            self._run_fixtures()
        except Pyro.errors.ConnectionClosedError:
            print >> sys.stderr, '[Testoob+Pyro pid=%d] child lost connection to parent, exiting' % os.getpid()
            sys.exit(1)

        sys.exit(0)