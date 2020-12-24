# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/twist.py
# Compiled at: 2009-09-07 12:56:49
"""Привязки к TwistedMatrix."""
import sys
threaded = False
FINISH_TIMEOUT = 5
import pkg_resources

def install(threaded=False, wxapp=None, poolsize=-1):
    globals = sys._getframe().f_globals
    globals['threaded'] = threaded
    pkg_resources.require('twisted')
    if wxapp:
        from twisted.internet import wxreactor
        wxreactor.install()
    else:
        try:
            from twisted.internet import epollreactor
            epollreactor.install()
        except:
            if sys.platform.startswith('win'):
                from twisted.internet import iocpreactor
                iocpreactor.install()
            else:
                try:
                    from twisted.internet import pollreactor
                    pollreactor.install()
                except:
                    from twisted.internet import selectreactor
                else:
                    selectreactor.install()

        from twisted.internet import reactor
        globals['reactor'] = reactor
        if wxapp:
            reactor.registerWxApp(wxapp)
        if threaded:
            from twisted.internet import threads
            globals['threads'] = threads
            from threading import Lock
            if poolsize > 0:
                reactor.suggestThreadPoolSize(poolsize)
        from twisted.internet import task
        globals['task'] = task
        from twisted.internet.defer import DeferredLock as Lock
    from twisted.internet import defer
    globals['deferred'] = defer
    globals['Lock'] = Lock
    defer.setDebugging(True)
    from twisted.python import log
    from twisted.python.log import msg
    globals['log'] = log
    globals['msg'] = msg


def defer(method, *args):
    u"""Возвращает объект результата отложенного вычисления."""
    if threaded:
        return threads.deferToThread(method, *args)
    else:
        return task.deferLater(reactor, 0, method, *args)


def asyncall(method, *args):
    u"""Просто запускает метод с немедленным возвратом."""
    if threaded:
        reactor.callInThread(method, *args)
    else:
        reactor.callLater(0, method, *args)


def syncall(method, *args):
    u"""Запускает метод и ожидает результатов исполнения."""
    if threaded:
        return threads.blockingCallFromThread(reactor, method, *args)
    else:
        return method(*args)


def nodummy(funcobj):

    def wrapper(dummy, *args, **kw):
        return funcobj(*args, **kw)

    wrapper.__name__ = funcobj.__name__
    return wrapper


def syncallback(dfr, method, *args):
    return dfr.addCallback(nodummy(syncall), method, *args)


def asyncallback(dfr, method, *args):
    return dfr.addCallback(nodummy(asyncall), method, *args)


def lockrun(lock, method, *args):
    acq = deferred.maybeDeferred(lock.acquire())
    acq.addCallback(nodummy(method), *args)
    acq.addCallback(lambda result: result if lock.release() else result)
    return acq


def wxrun():
    if activated:
        reactor.run()
    else:
        wxapp.MainLoop()