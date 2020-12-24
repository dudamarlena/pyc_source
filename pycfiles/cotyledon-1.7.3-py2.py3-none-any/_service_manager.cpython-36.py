# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /workspace/sileht/common/cotyledon/build/lib.linux-x86_64-2.7/cotyledon/_service_manager.py
# Compiled at: 2018-08-28 05:24:33
# Size of source mod 2**32: 15075 bytes
import collections, contextlib, logging, multiprocessing, os, signal, socket, sys, threading, time, uuid
from cotyledon import _service
from cotyledon import _utils
LOG = logging.getLogger(__name__)

class ServiceManager(_utils.SignalManager):
    __doc__ = "Manage lifetimes of services\n\n    :py:class:`ServiceManager` acts as a master process that controls the\n    lifetime of children processes and restart them if they die unexpectedly.\n    It also propagate some signals (SIGTERM, SIGALRM, SIGINT and SIGHUP) to\n    them.\n\n    Each child process (:py:class:`ServiceWorker`) runs an instance of\n    a :py:class:`Service`.\n\n    An application must create only one :py:class:`ServiceManager` class and\n    use :py:meth:`ServiceManager.run()` as main loop of the application.\n\n\n\n    Usage::\n\n        class MyService(Service):\n            def __init__(self, worker_id, myconf):\n                super(MyService, self).__init__(worker_id)\n                preparing_my_job(myconf)\n                self.running = True\n\n            def run(self):\n                while self.running:\n                    do_my_job()\n\n            def terminate(self):\n                self.running = False\n                gracefully_stop_my_jobs()\n\n            def reload(self):\n                restart_my_job()\n\n\n        class MyManager(ServiceManager):\n            def __init__(self):\n                super(MyManager, self).__init__()\n                self.register_hooks(on_reload=self.reload)\n\n                conf = {'foobar': 2}\n                self.service_id = self.add(MyService, 5, conf)\n\n            def reload(self):\n                self.reconfigure(self.service_id, 10)\n\n        MyManager().run()\n\n    This will create 5 children processes running the service MyService.\n\n    "
    _process_runner_already_created = False

    def __init__(self, wait_interval=0.01, graceful_shutdown_timeout=60):
        """Creates the ServiceManager object

        :param wait_interval: time between each new process spawn
        :type wait_interval: float

        """
        if self._process_runner_already_created:
            raise RuntimeError('Only one instance of ServiceManager per application is allowed')
        ServiceManager._process_runner_already_created = True
        super(ServiceManager, self).__init__()
        self._services = collections.OrderedDict()
        self._running_services = collections.defaultdict(dict)
        self._forktimes = []
        self._graceful_shutdown_timeout = graceful_shutdown_timeout
        self._wait_interval = wait_interval
        self._dead = threading.Event()
        self._got_sig_chld = threading.Event()
        self._got_sig_chld.set()
        self._child_supervisor = None
        self._hooks = {'terminate':[],  'reload':[],  'new_worker':[]}
        _utils.setproctitle('%s: master process [%s]' % (
         _utils.get_process_name(), ' '.join(sys.argv)))
        try:
            os.setsid()
        except (OSError, AttributeError):
            pass

        self._death_detection_pipe = multiprocessing.Pipe(duplex=False)
        signal.signal(signal.SIGINT, self._fast_exit)
        if os.name == 'posix':
            signal.signal(signal.SIGCHLD, self._signal_catcher)

    def register_hooks(self, on_terminate=None, on_reload=None, on_new_worker=None):
        """Register hook methods

        This can be callable multiple times to add more hooks, hooks are
        executed in added order. If a hook raised an exception, next hooks
        will be not executed.

        :param on_terminate: method called on SIGTERM
        :type on_terminate: callable()
        :param on_reload: method called on SIGHUP
        :type on_reload: callable()
        :param on_new_worker: method called in the child process when this one
                              is ready
        :type on_new_worker: callable(service_id, worker_id, service_obj)

        If window support is planned, hooks callable must support
        to be pickle.pickle(). See CPython multiprocessing module documentation
        for more detail.
        """
        if on_terminate is not None:
            _utils.check_callable(on_terminate, 'on_terminate')
            self._hooks['terminate'].append(on_terminate)
        else:
            if on_reload is not None:
                _utils.check_callable(on_reload, 'on_reload')
                self._hooks['reload'].append(on_reload)
            if on_new_worker is not None:
                _utils.check_callable(on_new_worker, 'on_new_worker')
                self._hooks['new_worker'].append(on_new_worker)

    def _run_hooks(self, name, *args, **kwargs):
        (_utils.run_hooks)(name, self._hooks[name], *args, **kwargs)

    def add(self, service, workers=1, args=None, kwargs=None):
        """Add a new service to the ServiceManager

        :param service: callable that return an instance of :py:class:`Service`
        :type service: callable
        :param workers: number of processes/workers for this service
        :type workers: int
        :param args: additional positional arguments for this service
        :type args: tuple
        :param kwargs: additional keywoard arguments for this service
        :type kwargs: dict

        :return: a service id
        :rtype: uuid.uuid4
        """
        _utils.check_callable(service, 'service')
        _utils.check_workers(workers, 1)
        service_id = uuid.uuid4()
        self._services[service_id] = _service.ServiceConfig(service_id, service, workers, args, kwargs)
        return service_id

    def reconfigure(self, service_id, workers):
        """Reconfigure a service registered in ServiceManager

        :param service_id: the service id
        :type service_id: uuid.uuid4
        :param workers: number of processes/workers for this service
        :type workers: int
        :raises: ValueError
        """
        try:
            sc = self._services[service_id]
        except KeyError:
            raise ValueError("%s service id doesn't exists" % service_id)
        else:
            _utils.check_workers(workers, minimum=(1 - sc.workers))
            sc.workers = workers
            self._forktimes = []

    def run(self):
        """Start and supervise services workers

        This method will start and supervise all children processes
        until the master process asked to shutdown by a SIGTERM.

        All spawned processes are part of the same unix process group.
        """
        self._systemd_notify_once()
        self._child_supervisor = _utils.spawn(self._child_supervisor_thread)
        self._wait_forever()

    def _child_supervisor_thread(self):
        while not self._dead.is_set():
            self._got_sig_chld.wait()
            self._got_sig_chld.clear()
            if self._dead.is_set():
                return
            info = self._get_last_worker_died()
            while info is not None:
                service_id, worker_id = info
                self._start_worker(service_id, worker_id)
                info = self._get_last_worker_died()
                if self._dead.is_set():
                    return

            self._adjust_workers()

    def _on_signal_received(self, sig):
        if sig == _utils.SIGALRM:
            self._alarm()
        else:
            if sig == signal.SIGTERM:
                self._shutdown()
            else:
                if sig == _utils.SIGHUP:
                    self._reload()
                else:
                    if sig == _utils.SIGCHLD:
                        self._got_sig_chld.set()
                    else:
                        LOG.debug('unhandled signal %s' % sig)

    def _alarm(self):
        self._fast_exit(reason='Graceful shutdown timeout exceeded, instantaneous exiting of master process')

    def _reload(self):
        """reload all children

        posix only
        """
        self._run_hooks('reload')
        self._forktimes = []
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        os.killpg(0, signal.SIGHUP)
        signal.signal(signal.SIGHUP, self._signal_catcher)

    def _shutdown(self):
        LOG.info('Caught SIGTERM signal, graceful exiting of master process')
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        if self._graceful_shutdown_timeout > 0:
            if os.name == 'posix':
                signal.alarm(self._graceful_shutdown_timeout)
            else:
                threading.Timer(self._graceful_shutdown_timeout, self._alarm).start()
        self._dead.set()
        self._got_sig_chld.set()
        self._child_supervisor.join()
        self._run_hooks('terminate')
        LOG.debug('Killing services with signal SIGTERM')
        if os.name == 'posix':
            os.killpg(0, signal.SIGTERM)
        LOG.debug('Waiting services to terminate')
        for processes in self._running_services.values():
            for process in processes:
                if os.name != 'posix':
                    process.terminate()
                process.join()

        LOG.debug('Shutdown finish')
        sys.exit(0)

    def _adjust_workers(self):
        for service_id, conf in self._services.items():
            running_workers = len(self._running_services[service_id])
            if running_workers < conf.workers:
                for worker_id in range(running_workers, conf.workers):
                    self._start_worker(service_id, worker_id)

            else:
                if running_workers > conf.workers:
                    for worker_id in range(running_workers, conf.workers):
                        self._stop_worker(service_id, worker_id)

    def _get_last_worker_died(self):
        """Return the last died worker information or None"""
        for service_id in list(self._running_services.keys()):
            processes = list(self._running_services[service_id].items())
            for process, worker_id in processes:
                if not process.is_alive():
                    if process.exitcode < 0:
                        sig = _utils.signal_to_name(process.exitcode)
                        LOG.info('Child %(pid)d killed by signal %(sig)s', dict(pid=(process.pid), sig=sig))
                    else:
                        LOG.info('Child %(pid)d exited with status %(code)d', dict(pid=(process.pid), code=(process.exitcode)))
                    del self._running_services[service_id][process]
                    return (service_id, worker_id)

    def _fast_exit(self, signo=None, frame=None, reason='Caught SIGINT signal, instantaneous exiting'):
        if os.name == 'posix':
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            LOG.info(reason)
            os.killpg(0, signal.SIGINT)
        else:
            LOG.info(reason)
        os._exit(1)

    def _slowdown_respawn_if_needed(self):
        expected_children = sum(s.workers for s in self._services.values())
        if len(self._forktimes) > expected_children:
            if time.time() - self._forktimes[0] < expected_children:
                LOG.info('Forking too fast, sleeping')
                time.sleep(5)
            self._forktimes.pop(0)
        else:
            time.sleep(self._wait_interval)
        self._forktimes.append(time.time())

    def _start_worker(self, service_id, worker_id):
        self._slowdown_respawn_if_needed()
        if os.name == 'posix':
            fds = [
             self.signal_pipe_w, self.signal_pipe_r]
        else:
            fds = []
        p = _utils.spawn_process((_service.ServiceWorker.create_and_wait),
          (self._services[service_id]),
          service_id,
          worker_id,
          (self._death_detection_pipe),
          (self._hooks['new_worker']),
          (self._graceful_shutdown_timeout),
          fds_to_close=fds)
        self._running_services[service_id][p] = worker_id

    def _stop_worker(self, service_id, worker_id):
        for process, _id in self._running_services[service_id].items():
            if _id == worker_id:
                process.terminte()

    @staticmethod
    def _systemd_notify_once():
        """Send notification once to Systemd that service is ready.

        Systemd sets NOTIFY_SOCKET environment variable with the name of the
        socket listening for notifications from services.
        This method removes the NOTIFY_SOCKET environment variable to ensure
        notification is sent only once.
        """
        notify_socket = os.getenv('NOTIFY_SOCKET')
        if notify_socket:
            if notify_socket.startswith('@'):
                notify_socket = '\x00%s' % notify_socket[1:]
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            with contextlib.closing(sock):
                try:
                    sock.connect(notify_socket)
                    sock.sendall(b'READY=1')
                    del os.environ['NOTIFY_SOCKET']
                except EnvironmentError:
                    LOG.debug('Systemd notification failed', exc_info=True)