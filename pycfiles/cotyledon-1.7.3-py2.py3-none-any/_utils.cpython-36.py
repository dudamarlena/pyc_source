# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /workspace/sileht/common/cotyledon/build/lib.linux-x86_64-2.7/cotyledon/_utils.py
# Compiled at: 2018-08-28 05:24:33
# Size of source mod 2**32: 6580 bytes
import collections, contextlib, errno, logging, multiprocessing, os, select, signal, sys, threading, time
if os.name == 'posix':
    import fcntl
else:
    LOG = logging.getLogger(__name__)
    _SIGNAL_TO_NAME = dict((getattr(signal, name), name) for name in dir(signal) if name.startswith('SIG') if name not in ('SIG_DFL',
                                                                                                                           'SIG_IGN'))

    def signal_to_name(sig):
        return _SIGNAL_TO_NAME.get(sig)


    def spawn(target, *args, **kwargs):
        t = threading.Thread(target=target, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t


    def check_workers(workers, minimum):
        if not isinstance(workers, int) or workers < minimum:
            raise ValueError("'workers' must be an int >= %d, not: %s (%s)" % (
             minimum, workers, type(workers).__name__))


    def check_callable(thing, name):
        if not hasattr(thing, '__call__'):
            raise ValueError("'%s' must be a callable" % name)


    def _bootstrap_process(target, *args, **kwargs):
        if 'fds_to_close' in kwargs:
            for fd in kwargs['fds_to_close']:
                os.close(fd)

            del kwargs['fds_to_close']
        target(*args, **kwargs)


    def spawn_process(*args, **kwargs):
        p = multiprocessing.Process(target=_bootstrap_process, args=args,
          kwargs=kwargs)
        p.start()
        return p


    try:
        from setproctitle import setproctitle
    except ImportError:

        def setproctitle(*args, **kwargs):
            pass


    def get_process_name():
        return os.path.basename(sys.argv[0])


    def run_hooks(name, hooks, *args, **kwargs):
        try:
            for hook in hooks:
                hook(*args, **kwargs)

        except Exception:
            LOG.exception('Exception raised during %s hooks' % name)


    @contextlib.contextmanager
    def exit_on_exception():
        try:
            yield
        except SystemExit as exc:
            os._exit(exc.code)
        except BaseException:
            LOG.exception('Unhandled exception')
            os._exit(2)


    if os.name == 'posix':
        SIGALRM = signal.SIGALRM
        SIGHUP = signal.SIGHUP
        SIGCHLD = signal.SIGCHLD
        SIBREAK = None
    else:
        SIGALRM = SIGHUP = None
    SIGCHLD = 'fake sigchld'
    SIGBREAK = signal.SIGBREAK

class SignalManager(object):

    def __init__(self):
        if os.name == 'posix':
            self.signal_pipe_r, self.signal_pipe_w = os.pipe()
            self._set_nonblock(self.signal_pipe_r)
            self._set_nonblock(self.signal_pipe_w)
            signal.set_wakeup_fd(self.signal_pipe_w)
        else:
            self._signals_received = collections.deque()
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            if os.name == 'posix':
                signal.signal(signal.SIGCHLD, signal.SIG_DFL)
                signal.signal(signal.SIGTERM, self._signal_catcher)
                signal.signal(signal.SIGALRM, self._signal_catcher)
                signal.signal(signal.SIGHUP, self._signal_catcher)
            else:
                signal.signal(signal.SIGTERM, self._signal_catcher)
                signal.signal(signal.SIGBREAK, self._signal_catcher)

    @staticmethod
    def _set_nonblock(fd):
        flags = fcntl.fcntl(fd, fcntl.F_GETFL, 0)
        flags = flags | os.O_NONBLOCK
        fcntl.fcntl(fd, fcntl.F_SETFL, flags)

    def _signal_catcher(self, sig, frame):
        if sig in (SIGALRM, signal.SIGTERM):
            self._signals_received.appendleft(sig)
        else:
            self._signals_received.append(sig)

    def _wait_forever(self):
        while True:
            if os.name == 'posix':
                self._empty_signal_pipe()
            self._run_signal_handlers()
            if os.name == 'posix':
                try:
                    select.select([self.signal_pipe_r], [], [])
                except select.error as e:
                    if e.args[0] != errno.EINTR:
                        raise

            else:
                time.sleep(1)
                self._signals_received.append(SIGCHLD)

    def _empty_signal_pipe(self):
        try:
            while os.read(self.signal_pipe_r, 4096) == 4096:
                pass

        except (IOError, OSError):
            pass

    def _run_signal_handlers(self):
        while True:
            try:
                sig = self._signals_received.popleft()
            except IndexError:
                return
            else:
                self._on_signal_received(sig)

    def _on_signal_received(self, sig):
        pass