# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/platform/twisted.py
# Compiled at: 2012-01-23 23:44:33
"""A Twisted reactor built on the Tornado IOLoop.

This module lets you run applications and libraries written for
Twisted in a Tornado application.  To use it, simply call `install` at
the beginning of the application::

    import tornado.platform.twisted
    tornado.platform.twisted.install()
    from twisted.internet import reactor

When the app is ready to start, call `IOLoop.instance().start()`
instead of `reactor.run()`.  This will allow you to use a mixture of
Twisted and Tornado code in the same process.

It is also possible to create a non-global reactor by calling
`tornado.platform.twisted.TornadoReactor(io_loop)`.  However, if
the `IOLoop` and reactor are to be short-lived (such as those used in
unit tests), additional cleanup may be required.  Specifically, it is
recommended to call::

    reactor.fireSystemEvent('shutdown')
    reactor.disconnectAll()

before closing the `IOLoop`.

This module has been tested with Twisted versions 11.0.0 and 11.1.0.
"""
from __future__ import with_statement, absolute_import
import functools, logging, time
from twisted.internet.posixbase import PosixReactorBase
from twisted.internet.interfaces import IReactorFDSet, IDelayedCall, IReactorTime
from twisted.python import failure, log
from twisted.internet import error
from zope.interface import implements
import tornado, tornado.ioloop
from tornado.stack_context import NullContext
from tornado.ioloop import IOLoop

class TornadoDelayedCall(object):
    """DelayedCall object for Tornado."""
    implements(IDelayedCall)

    def __init__(self, reactor, seconds, f, *args, **kw):
        self._reactor = reactor
        self._func = functools.partial(f, *args, **kw)
        self._time = self._reactor.seconds() + seconds
        self._timeout = self._reactor._io_loop.add_timeout(self._time, self._called)
        self._active = True

    def _called(self):
        self._active = False
        self._reactor._removeDelayedCall(self)
        try:
            self._func()
        except:
            logging.error('_called caught exception', exc_info=True)

    def getTime(self):
        return self._time

    def cancel(self):
        self._active = False
        self._reactor._io_loop.remove_timeout(self._timeout)
        self._reactor._removeDelayedCall(self)

    def delay(self, seconds):
        self._reactor._io_loop.remove_timeout(self._timeout)
        self._time += seconds
        self._timeout = self._reactor._io_loop.add_timeout(self._time, self._called)

    def reset(self, seconds):
        self._reactor._io_loop.remove_timeout(self._timeout)
        self._time = self._reactor.seconds() + seconds
        self._timeout = self._reactor._io_loop.add_timeout(self._time, self._called)

    def active(self):
        return self._active


class TornadoReactor(PosixReactorBase):
    """Twisted reactor built on the Tornado IOLoop.

    Since it is intented to be used in applications where the top-level
    event loop is ``io_loop.start()`` rather than ``reactor.run()``,
    it is implemented a little differently than other Twisted reactors.
    We override `mainLoop` instead of `doIteration` and must implement
    timed call functionality on top of `IOLoop.add_timeout` rather than
    using the implementation in `PosixReactorBase`.
    """
    implements(IReactorTime, IReactorFDSet)

    def __init__(self, io_loop=None):
        if not io_loop:
            io_loop = tornado.ioloop.IOLoop.instance()
        self._io_loop = io_loop
        self._readers = {}
        self._writers = {}
        self._fds = {}
        self._delayedCalls = {}
        PosixReactorBase.__init__(self)

        def start_if_necessary():
            if not self._started:
                self.fireSystemEvent('startup')

        self._io_loop.add_callback(start_if_necessary)

    def seconds(self):
        return time.time()

    def callLater(self, seconds, f, *args, **kw):
        dc = TornadoDelayedCall(self, seconds, f, *args, **kw)
        self._delayedCalls[dc] = True
        return dc

    def getDelayedCalls(self):
        return [ x for x in self._delayedCalls if x._active ]

    def _removeDelayedCall(self, dc):
        if dc in self._delayedCalls:
            del self._delayedCalls[dc]

    def callFromThread(self, f, *args, **kw):
        """See `twisted.internet.interfaces.IReactorThreads.callFromThread`"""
        assert callable(f), '%s is not callable' % f
        p = functools.partial(f, *args, **kw)
        self._io_loop.add_callback(p)

    def installWaker(self):
        pass

    def wakeUp(self):
        pass

    def _invoke_callback(self, fd, events):
        reader, writer = self._fds[fd]
        if reader:
            err = None
            if reader.fileno() == -1:
                err = error.ConnectionLost()
            elif events & IOLoop.READ:
                err = log.callWithLogger(reader, reader.doRead)
            if err is None and events & IOLoop.ERROR:
                err = error.ConnectionLost()
            if err is not None:
                self.removeReader(reader)
                reader.readConnectionLost(failure.Failure(err))
        if writer:
            err = None
            if writer.fileno() == -1:
                err = error.ConnectionLost()
            elif events & IOLoop.WRITE:
                err = log.callWithLogger(writer, writer.doWrite)
            if err is None and events & IOLoop.ERROR:
                err = error.ConnectionLost()
            if err is not None:
                self.removeWriter(writer)
                writer.writeConnectionLost(failure.Failure(err))
        return

    def addReader(self, reader):
        """Add a FileDescriptor for notification of data available to read."""
        if reader in self._readers:
            return
        else:
            fd = reader.fileno()
            self._readers[reader] = fd
            if fd in self._fds:
                _, writer = self._fds[fd]
                self._fds[fd] = (reader, writer)
                if writer:
                    self._io_loop.update_handler(fd, IOLoop.READ | IOLoop.WRITE)
            else:
                with NullContext():
                    self._fds[fd] = (
                     reader, None)
                    self._io_loop.add_handler(fd, self._invoke_callback, IOLoop.READ)
            return

    def addWriter(self, writer):
        """Add a FileDescriptor for notification of data available to write."""
        if writer in self._writers:
            return
        else:
            fd = writer.fileno()
            self._writers[writer] = fd
            if fd in self._fds:
                reader, _ = self._fds[fd]
                self._fds[fd] = (reader, writer)
                if reader:
                    self._io_loop.update_handler(fd, IOLoop.READ | IOLoop.WRITE)
            else:
                with NullContext():
                    self._fds[fd] = (
                     None, writer)
                    self._io_loop.add_handler(fd, self._invoke_callback, IOLoop.WRITE)
            return

    def removeReader(self, reader):
        """Remove a Selectable for notification of data available to read."""
        if reader in self._readers:
            fd = self._readers.pop(reader)
            _, writer = self._fds[fd]
            if writer:
                self._fds[fd] = (
                 None, writer)
                self._io_loop.update_handler(fd, IOLoop.WRITE)
            else:
                del self._fds[fd]
                self._io_loop.remove_handler(fd)
        return

    def removeWriter(self, writer):
        """Remove a Selectable for notification of data available to write."""
        if writer in self._writers:
            fd = self._writers.pop(writer)
            reader, _ = self._fds[fd]
            if reader:
                self._fds[fd] = (
                 reader, None)
                self._io_loop.update_handler(fd, IOLoop.READ)
            else:
                del self._fds[fd]
                self._io_loop.remove_handler(fd)
        return

    def removeAll(self):
        return self._removeAll(self._readers, self._writers)

    def getReaders(self):
        return self._readers.keys()

    def getWriters(self):
        return self._writers.keys()

    def stop(self):
        PosixReactorBase.stop(self)
        self._io_loop.stop()

    def crash(self):
        PosixReactorBase.crash(self)
        self._io_loop.stop()

    def doIteration(self, delay):
        raise NotImplementedError('doIteration')

    def mainLoop(self):
        self._io_loop.start()
        if self._stopped:
            self.fireSystemEvent('shutdown')


class _TestReactor(TornadoReactor):
    """Subclass of TornadoReactor for use in unittests.

    This can't go in the test.py file because of import-order dependencies
    with the Twisted reactor test builder.
    """

    def __init__(self):
        super(_TestReactor, self).__init__(IOLoop())

    def listenTCP(self, port, factory, backlog=50, interface=''):
        if not interface:
            interface = '127.0.0.1'
        return super(_TestReactor, self).listenTCP(port, factory, backlog=backlog, interface=interface)

    def listenUDP(self, port, protocol, interface='', maxPacketSize=8192):
        if not interface:
            interface = '127.0.0.1'
        return super(_TestReactor, self).listenUDP(port, protocol, interface=interface, maxPacketSize=maxPacketSize)


def install(io_loop=None):
    """Install this package as the default Twisted reactor."""
    if not io_loop:
        io_loop = tornado.ioloop.IOLoop.instance()
    reactor = TornadoReactor(io_loop)
    from twisted.internet.main import installReactor
    installReactor(reactor)
    return reactor