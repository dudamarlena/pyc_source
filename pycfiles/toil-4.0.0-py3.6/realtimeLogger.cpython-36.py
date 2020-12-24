# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/realtimeLogger.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 9540 bytes
"""
Implements a real-time UDP-based logging system that user scripts can use for debugging.
"""
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
from builtins import super
import os, os.path, json, logging, logging.handlers, threading
from six.moves import socketserver as SocketServer
from future.utils import with_metaclass
import toil.lib.bioio
from toil.batchSystems.options import getPublicIP
log = logging.getLogger(__name__)

class LoggingDatagramHandler(SocketServer.BaseRequestHandler):
    __doc__ = '\n    Receive logging messages from the jobs and display them on the leader.\n    \n    Uses bare JSON message encoding.\n    '

    def handle(self):
        """
        Handle a single message. SocketServer takes care of splitting out the messages.
        
        Messages are JSON-encoded logging module records.
        """
        data, socket = self.request
        try:
            message_attrs = json.loads(data.decode('utf-8'))
            record = logging.makeLogRecord(message_attrs)
            if isinstance(record.args, list):
                record.args = tuple(record.args)
        except:
            logging.error('Malformed log message from {}'.format(self.client_address[0]))
        else:
            log.handle(record)


class JSONDatagramHandler(logging.handlers.DatagramHandler):
    __doc__ = "\n    Send logging records over UDP serialized as JSON.\n    \n    They have to fit in a single UDP datagram, so don't try to log more than 64kb at once.\n    "

    def makePickle(self, record):
        """
        Actually, encode the record as bare JSON instead.
        """
        return json.dumps(record.__dict__).encode('utf-8')


class RealtimeLoggerMetaclass(type):
    __doc__ = '\n    Metaclass for RealtimeLogger that lets you do things like RealtimeLogger.warning(),\n    RealtimeLogger.info(), etc.\n    '

    def __getattr__(self, name):
        """
        If a real attribute can't be found, try one of the logging methods on the actual logger
        object.
        """
        return getattr(self.getLogger(), name)


class RealtimeLogger(with_metaclass(RealtimeLoggerMetaclass, object)):
    __doc__ = '\n    Provides a logger that logs over UDP to the leader. To use in a Toil job, do:\n\n    >>> from toil.realtimeLogger import RealtimeLogger\n    >>> RealtimeLogger.info("This logging message goes straight to the leader")\n\n    That\'s all a user of Toil would need to do. On the leader, Job.Runner.startToil()\n    automatically starts the UDP server by using an instance of this class as a context manager.\n    '
    envPrefix = 'TOIL_RT_LOGGING_'
    defaultLevel = 'INFO'
    lock = threading.RLock()
    loggingServer = None
    serverThread = None
    initialized = 0
    logger = None

    @classmethod
    def _startLeader(cls, batchSystem, level=defaultLevel):
        with cls.lock:
            if cls.initialized == 0:
                cls.initialized += 1
                if level:
                    log.info('Starting real-time logging.')
                    cls.loggingServer = SocketServer.ThreadingUDPServer(server_address=('0.0.0.0',
                                                                                        0),
                      RequestHandlerClass=LoggingDatagramHandler)
                    cls.serverThread = threading.Thread(target=(cls.loggingServer.serve_forever))
                    cls.serverThread.daemon = True
                    cls.serverThread.start()
                    ip = getPublicIP()
                    port = cls.loggingServer.server_address[1]

                    def _setEnv(name, value):
                        name = cls.envPrefix + name
                        os.environ[name] = value
                        batchSystem.setEnv(name)

                    _setEnv('ADDRESS', '%s:%i' % (ip, port))
                    _setEnv('LEVEL', level)
                else:
                    log.debug('Real-time logging disabled')
            else:
                if level:
                    log.warning('Ignoring nested request to start real-time logging')

    @classmethod
    def _stopLeader(cls):
        """
        Stop the server on the leader.
        """
        with cls.lock:
            assert cls.initialized > 0
            cls.initialized -= 1
            if cls.initialized == 0:
                if cls.loggingServer:
                    log.info('Stopping real-time logging server.')
                    cls.loggingServer.shutdown()
                    cls.loggingServer = None
                if cls.serverThread:
                    log.info('Joining real-time logging server thread.')
                    cls.serverThread.join()
                    cls.serverThread = None
                for k in list(os.environ.keys()):
                    if k.startswith(cls.envPrefix):
                        os.environ.pop(k)

    @classmethod
    def getLogger(cls):
        """
        Get the logger that logs real-time to the leader.
        
        Note that if the returned logger is used on the leader, you will see the message twice,
        since it still goes to the normal log handlers, too.
        """
        if cls.logger is None:
            with cls.lock:
                if cls.logger is None:
                    cls.logger = logging.getLogger('toil-rt')
                    try:
                        level = os.environ[(cls.envPrefix + 'LEVEL')]
                    except KeyError:
                        cls.logger.setLevel(logging.CRITICAL)
                    else:
                        toil.lib.bioio.setLogLevel(level, cls.logger)
                        try:
                            address = os.environ[(cls.envPrefix + 'ADDRESS')]
                        except KeyError:
                            pass
                        else:
                            host, port = address.split(':')
                            cls.logger.addHandler(JSONDatagramHandler(host, int(port)))
        return cls.logger

    def __init__(self, batchSystem, level=defaultLevel):
        """
        A context manager that starts up the UDP server.

        Should only be invoked on the leader. Python logging should have already been configured.
        This method takes an optional log level, as a string level name, from the set supported
        by bioio. If the level is None, False or the empty string, real-time logging will be
        disabled, i.e. no UDP server will be started on the leader and log messages will be
        suppressed on the workers. Note that this is different from passing level='OFF',
        which is equivalent to level='CRITICAL' and does not disable the server.
        """
        super().__init__()
        self._RealtimeLogger__level = level
        self._RealtimeLogger__batchSystem = batchSystem

    def __enter__(self):
        RealtimeLogger._startLeader((self._RealtimeLogger__batchSystem), level=(self._RealtimeLogger__level))

    def __exit__(self, exc_type, exc_val, exc_tb):
        RealtimeLogger._stopLeader()