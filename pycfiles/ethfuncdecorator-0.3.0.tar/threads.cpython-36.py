# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/threads.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 3280 bytes
"""
A minimal implementation of the various gevent APIs used within this codebase.
"""
import threading, time

class Timeout(Exception):
    __doc__ = '\n    A limited subset of the `gevent.Timeout` context manager.\n    '
    seconds = None
    exception = None
    begun_at = None
    is_running = None

    def __init__(self, seconds=None, exception=None, *args, **kwargs):
        self.seconds = seconds
        self.exception = exception

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __str__(self):
        if self.seconds is None:
            return ''
        else:
            return '{0} seconds'.format(self.seconds)

    @property
    def expire_at(self):
        if self.seconds is None:
            raise ValueError('Timeouts with `seconds == None` do not have an expiration time')
        else:
            if self.begun_at is None:
                raise ValueError('Timeout has not been started')
        return self.begun_at + self.seconds

    def start(self):
        if self.is_running is not None:
            raise ValueError('Timeout has already been started')
        self.begun_at = time.time()
        self.is_running = True

    def check(self):
        if self.is_running is None:
            raise ValueError('Timeout has not been started')
        else:
            if self.is_running is False:
                raise ValueError('Timeout has already been cancelled')
            else:
                if self.seconds is None:
                    return
        if time.time() > self.expire_at:
            self.is_running = False
            if isinstance(self.exception, type):
                raise self.exception(str(self))
            else:
                if isinstance(self.exception, Exception):
                    raise self.exception
                else:
                    raise self

    def cancel(self):
        self.is_running = False

    def sleep(self, seconds):
        time.sleep(seconds)
        self.check()


class ThreadWithReturn(threading.Thread):

    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__(target=target,
          args=(args or tuple()),
          kwargs=(kwargs or {}))
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self._return = (self.target)(*self.args, **self.kwargs)

    def get(self, timeout=None):
        self.join(timeout)
        try:
            return self._return
        except AttributeError:
            raise RuntimeError('Something went wrong.  No `_return` property was set')


class TimerClass(threading.Thread):

    def __init__(self, interval, callback, *args):
        threading.Thread.__init__(self)
        self.callback = callback
        self.terminate_event = threading.Event()
        self.interval = interval
        self.args = args

    def run(self):
        while not self.terminate_event.is_set():
            (self.callback)(*self.args)
            self.terminate_event.wait(self.interval)

    def stop(self):
        self.terminate_event.set()


def spawn(target, *args, thread_class=ThreadWithReturn, **kwargs):
    thread = thread_class(target=target,
      args=args,
      kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread