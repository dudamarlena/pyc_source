# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /workspace/sileht/common/cotyledon/build/lib.linux-x86_64-2.7/cotyledon/_service.py
# Compiled at: 2018-08-28 05:24:33
# Size of source mod 2**32: 8126 bytes
import logging, os, random, signal, sys, threading
from cotyledon import _utils
LOG = logging.getLogger(__name__)

class Service(object):
    """Service"""
    name = None
    graceful_shutdown_timeout = None

    def __init__(self, worker_id):
        super(Service, self).__init__()
        self._initialize(worker_id)

    def _initialize(self, worker_id):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        if self.name is None:
            self.name = self.__class__.__name__
        self.worker_id = worker_id
        self.pid = os.getpid()
        self._signal_lock = threading.Lock()
        self._on_reload_internal_hook = self._noop_hook

    def _noop_hook(self, service):
        pass

    def terminate(self):
        """Gracefully shutdown the service

        This method will be executed when the Service has to shutdown cleanly.

        If not implemented the process will just end with status 0.

        To customize the exit code, the :py:class:`SystemExit` exception can be
        used.

        Any exceptions raised by this method will be logged and the worker will
        exit with status 1.
        """
        pass

    def reload(self):
        """Reloading of the service

        This method will be executed when the Service receives a SIGHUP.

        If not implemented the process will just end with status 0 and
        :py:class:`ServiceRunner` will start a new fresh process for this
        service with the same worker_id.

        Any exceptions raised by this method will be logged and the worker will
        exit with status 1.
        """
        os.kill(os.getpid(), signal.SIGTERM)

    def run(self):
        """Method representing the service activity

        If not implemented the process will just wait to receive an ending
        signal.

        This method is ran into the thread and can block or return as needed

        Any exceptions raised by this method will be logged and the worker will
        exit with status 1.
        """
        pass

    def _reload(self):
        with _utils.exit_on_exception():
            if self._signal_lock.acquire(False):
                try:
                    self._on_reload_internal_hook(self)
                    self.reload()
                finally:
                    self._signal_lock.release()

    def _terminate(self):
        with _utils.exit_on_exception():
            with self._signal_lock:
                self.terminate()
                sys.exit(0)

    def _run(self):
        with _utils.exit_on_exception():
            self.run()


class ServiceConfig(object):

    def __init__(self, service_id, service, workers, args, kwargs):
        self.service = service
        self.workers = workers
        self.args = args
        self.kwargs = kwargs
        self.service_id = service_id


class ServiceWorker(_utils.SignalManager):
    """ServiceWorker"""

    @classmethod
    def create_and_wait(cls, *args, **kwargs):
        sw = cls(*args, **kwargs)
        sw.wait_forever()

    def __init__(self, config, service_id, worker_id, parent_pipe, started_hooks, graceful_shutdown_timeout):
        super(ServiceWorker, self).__init__()
        self._ready = threading.Event()
        _utils.spawn(self._watch_parent_process, parent_pipe)
        random.seed()
        args = tuple() if config.args is None else config.args
        kwargs = dict() if config.kwargs is None else config.kwargs
        self.service = (config.service)(worker_id, *args, **kwargs)
        self.service._initialize(worker_id)
        if self.service.graceful_shutdown_timeout is None:
            self.service.graceful_shutdown_timeout = graceful_shutdown_timeout
        self.title = '%(name)s(%(worker_id)d) [%(pid)d]' % dict(name=(self.service.name),
          worker_id=worker_id,
          pid=(os.getpid()))
        _utils.setproctitle('%(pname)s: %(name)s worker(%(worker_id)d)' % dict(pname=(_utils.get_process_name()),
          name=(self.service.name),
          worker_id=worker_id))
        self._ready.set()
        _utils.run_hooks('new_worker', started_hooks, service_id, worker_id, self.service)

    def _watch_parent_process(self, parent_pipe):
        parent_pipe[1].close()
        try:
            parent_pipe[0].recv()
        except EOFError:
            pass

        if self._ready.is_set():
            LOG.info('Parent process has died unexpectedly, %s exiting' % self.title)
            if os.name == 'posix':
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                self._signals_received.appendleft(signal.SIGTERM)
        else:
            os._exit(0)

    def _alarm(self):
        LOG.info('Graceful shutdown timeout (%d) exceeded, exiting %s now.' % (
         self.service.graceful_shutdown_timeout,
         self.title))
        os._exit(1)

    def _on_signal_received(self, sig):
        if sig == _utils.SIGALRM:
            self._alarm()
        else:
            if sig == signal.SIGTERM:
                LOG.info('Caught SIGTERM signal, graceful exiting of service %s' % self.title)
                if self.service.graceful_shutdown_timeout > 0:
                    if os.name == 'posix':
                        signal.alarm(self.service.graceful_shutdown_timeout)
                    else:
                        threading.Timer(self.service.graceful_shutdown_timeout, self._alarm).start()
                _utils.spawn(self.service._terminate)
            elif sig == _utils.SIGHUP:
                _utils.spawn(self.service._reload)

    def wait_forever(self):
        LOG.debug('Run service %s' % self.title)
        _utils.spawn(self.service._run)
        super(ServiceWorker, self)._wait_forever()