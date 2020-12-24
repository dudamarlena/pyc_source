# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kiddiepool/exceptions.py
# Compiled at: 2018-03-12 18:55:50
try:
    import queue
except ImportError:
    import Queue as queue

import socket

class KiddieException(Exception):
    """Base class for Kiddie Exceptions"""
    pass


class KiddiePoolEmpty(KiddieException, queue.Empty):
    """No Kiddie connections available in pool (even after timeout)"""
    pass


class KiddiePoolMaxAttempts(KiddieException, socket.error):
    """Unable to connect to any Kiddie servers (even after timeout & retries)
    """
    pass


class KiddieSocketError(socket.error):
    """Base class for KiddieClientSend/Recv failures."""
    pass


class KiddieConnectionSendFailure(KiddieSocketError):
    """ KiddieConnection failed to send request """
    pass


class KiddieConnectionRecvFailure(KiddieSocketError):
    """ KiddieConnection failed to receive response """
    pass


class KiddieClientSendFailure(KiddieConnectionSendFailure):
    """KiddieClient failed to send request"""
    pass


class KiddieClientRecvFailure(KiddieConnectionRecvFailure):
    """KiddieClient failed to receive response"""
    pass


class TidePoolException(KiddieException):
    """KiddieException subclass for grouping TidePool errors."""
    pass


class TidePoolAlreadyBoundError(TidePoolException):
    """Attempted to bind a bound TidePool"""
    pass


class TidePoolAlreadyUnboundError(TidePoolException):
    """Attempted to unbind an unbound TidePool"""
    pass


class TidePoolBindError(TidePoolException):
    """Failed to bind TidePool to zk_session."""
    pass