# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data/code/pracmln/python3/pracmln/utils/multicore.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 2707 bytes
import multiprocessing
from multiprocessing import pool
import traceback, sys, signal, os
from ..mln.errors import OutOfMemoryError
import psutil

class CtrlCException(Exception):
    pass


class with_tracing(object):
    """with_tracing"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        signal.signal(signal.SIGINT, signal_handler)
        try:
            result = (self.func)(*args, **kwargs)
            return result
        except CtrlCException:
            pass
        except Exception as e:
            traceback.print_exc()
            raise e


def signal_handler(signal, frame):
    sys.stderr.write('Terminating process %s.\n' % os.getpid())
    raise CtrlCException()
    sys.exit(0)


class _methodcaller:
    """_methodcaller"""

    def __init__(self, method, sideeffects=False):
        self.method = method
        self.sideeffects = sideeffects

    def __call__(self, args):
        checkmem()
        if type(args) is list or type(args) is tuple:
            inst = args[0]
            args = args[1:]
        else:
            inst = args
            args = []
        if self.sideeffects:
            ret = (getattr(inst, self.method))(*args)
            return (
             ret, inst.__dict__)
        else:
            return (getattr(inst, self.method))(*args)


def checkmem():
    if float(psutil.virtual_memory().percent) > 75.0:
        raise OutOfMemoryError('Aborting due to excessive memory consumption.')


def make_memsafe():
    if sys.platform.startswith('linux'):
        import resource, psutil
        for rsrc in (resource.RLIMIT_AS, resource.RLIMIT_DATA):
            freemem = psutil.virtual_memory().free
            hard = int(round(freemem * 0.8))
            soft = hard
            resource.setrlimit(rsrc, (soft, hard))


class NoDaemonProcess(multiprocessing.Process):

    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonicPool(pool.Pool):
    Process = NoDaemonProcess


if __name__ == '__main__':

    def f(x):
        return x * x


    pool = multiprocessing.Pool(processes=4)
    print(pool.map(with_tracing(f), list(range(10))))