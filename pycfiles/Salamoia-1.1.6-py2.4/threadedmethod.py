# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/threadedmethod.py
# Compiled at: 2007-12-02 16:26:56
__all__ = [
 'threadmethod', 'ThreadMethodTimeoutError']

class ThreadMethodTimeoutError(Exception):
    __module__ = __name__


from threading import Thread

class ThreadMethodThread(Thread):
    """ThreadMethodThread, daemonic descendant class of threading.Thread which simply runs the specified target method with the specified arguments."""
    __module__ = __name__

    def __init__(self, target, args, kwargs):
        Thread.__init__(self)
        self.setDaemon(True)
        self.target, self.args, self.kwargs = target, args, kwargs
        self.start()

    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception, e:
            self.exception = e
        except:
            self.exception = Exception()
        else:
            self.exception = None

        return


def threadmethod(timeout=None):
    """@threadmethod(timeout), decorator function, returns a method wrapper which runs the wrapped method in a separate new thread."""

    def threadmethod_proxy(method):
        if hasattr(method, '__name__'):
            method_name = method.__name__
        else:
            method_name = 'unknown'

        def threadmethod_invocation_proxy(*args, **kwargs):
            worker = ThreadMethodThread(method, args, kwargs)
            if timeout is None:
                return
            worker.join(timeout)
            if worker.isAlive():
                raise ThreadMethodTimeoutError('A call to %s() has timed out' % method_name)
            elif worker.exception is not None:
                raise worker.exception
            else:
                return worker.result
            return

        threadmethod_invocation_proxy.__name__ = method_name
        return threadmethod_invocation_proxy

    return threadmethod_proxy


from salamoia.tests import *
runDocTests()