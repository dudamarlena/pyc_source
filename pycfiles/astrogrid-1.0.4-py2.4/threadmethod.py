# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/threadmethod.py
# Compiled at: 2007-03-24 03:32:03
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
                return worker
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


if __name__ == '__main__':
    print 'self-testing module threadmethod.py:'
    from threading import currentThread
    mainthread = currentThread()

    @threadmethod(5)
    def tryme():
        assert currentThread() is not mainthread


    tryme()

    @threadmethod(5)
    def foo(a, b, c):
        return a + b + c


    assert foo(1, 2, 3) == 6

    @threadmethod(5)
    def foo(*args):
        assert args == ('foo', )
        return args[0]


    assert foo('foo') == 'foo'

    @threadmethod(5)
    def foo(**kwargs):
        assert kwargs == {'foo': 'bar'}
        return kwargs['foo']


    assert foo(foo='bar') == 'bar'

    @threadmethod(5)
    def foo(a, b, *args, **kwargs):
        assert a == 1 and b == 'foo' and args == ('bar', ) and kwargs == {'biz': 'baz'}


    assert foo(1, 'foo', 'bar', biz='baz') is None
    from time import sleep

    class bar(object):
        __module__ = __name__

        @threadmethod(3)
        def __init__(self, timeout):
            sleep(timeout)

        @threadmethod(1)
        def throw(self, e):
            raise e


    try:
        bar(5)
    except ThreadMethodTimeoutError:
        pass
    else:
        assert False, 'Constructor should have timed out'

    try:
        bar(1).throw(IOError('fatal'))
    except IOError, e:
        assert str(e) == 'fatal'
    else:
        assert False, 'Expected IOError("fatal")'

    x = 0

    @threadmethod()
    def async():
        global x
        sleep(0.25)
        x += 1


    async()
    while x == 0:
        pass

    @threadmethod()
    def foo():
        sleep(1.0)


    foo().join()
    print 'ok'