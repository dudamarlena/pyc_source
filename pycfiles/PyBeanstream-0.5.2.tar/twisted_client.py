# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/beanstalk/twisted_client.py
# Compiled at: 2015-07-11 09:52:37
from twisted.protocols import basic
from twisted.internet import defer, protocol
from twisted.logger import Logger
import protohandler
try:
    from collections import deque
except ImportError:

    class deque(list):

        def popleft(self):
            return self.pop(0)

        def appendleft(self, item):
            self.insert(0, item)


class Command(object):
    """
    Wrap a client action into an object, that holds the values used in the
    protocol.

    @ivar _deferred: the L{Deferred} object that will be fired when the result
        arrives.
    @type _deferred: L{Deferred}

    @ivar command: name of the command sent to the server.
    @type command: C{str}
    """

    def __init__(self, command, handler, **kwargs):
        """
        Create a command.

        @param command: the name of the command.
        @type command: C{str}

        @param kwargs: this values will be stored as attributes of the object
            for future use
        """
        self.command = command
        self.handler = handler
        self._deferred = defer.Deferred()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<Command: %s>' % self.command

    def success(self, value):
        """
        Shortcut method to fire the underlying deferred.
        """
        self._deferred.callback(value)

    def fail(self, error):
        """
        Make the underlying deferred fails.
        """
        self._deferred.errback(error)


class Beanstalk(basic.LineReceiver):
    logger = Logger()

    def __init__(self):
        self._current = deque()

    def connectionMade(self):
        print 'Connected!'
        self.setLineMode()

    def __getattr__(self, attr):

        def caller(*args, **kw):
            return self.__cmd(attr, *getattr(protohandler, 'process_%s' % attr)(*args, **kw))

        try:
            getattr(protohandler, 'process_%s' % attr)
            return caller
        except:
            raise AttributeError(attr)

    def __cmd(self, command, full_command, handler):
        self.transport.write(full_command)
        cmdObj = Command(command, handler)
        self._current.append(cmdObj)
        return cmdObj._deferred

    def lineReceived(self, line):
        """
        Receive line commands from the server.
        """
        pending = self._current.popleft()
        try:
            res = pending.handler(line + '\r\n')
        except Exception as e:
            pending.fail(e)

        if res is not None:
            pending.success(res)
        else:
            self._current.appendleft(pending)
            self.setRawMode()
        return

    def rawDataReceived(self, data):
        pending = self._current.popleft()
        if len(data) >= pending.handler.remaining:
            rem = data[pending.handler.remaining:]
            data = data[:pending.handler.remaining]
        else:
            rem = None
        try:
            res = pending.handler(data)
        except Exception as e:
            pending.fail(e)
            self.setLineMode(rem)

        if res:
            pending.success(res)
            self.setLineMode(rem)
        else:
            self._current.appendleft(pending)
        return


class BeanstalkClientFactory(protocol.ClientFactory):
    logger = Logger()

    def startedConnecting(self, connector):
        self.logger.debug('{msg}', msg='Started to connect.')

    def buildProtocol(self, addr):
        self.logger.debug('{msg}', msg='Connected.')
        return Beanstalk()

    def clientConnectionLost(self, connector, reason):
        self.logger.debug('{msg}', msg='Lost connection, reason: ' % reason)

    def clientConnectionFailed(self, connector, reason):
        self.logger.debug('{msg}', msg='Connection failed, reason: ' % reason)