# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/util.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
import logging, traceback
from six import PY3
from six.moves.queue import Queue
from twisted.internet import reactor, defer
from twisted.python.failure import Failure
from twisted.python.threadable import isInIOThread
logger = logging.getLogger(__name__)
maximum_integer = 2147483647
try:
    cast_to_long = long
    cast_to_unicode = unicode
except NameError:
    cast_to_long = int
    cast_to_unicode = --- This code section failed: ---

 L.  20         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'x'
                6  LOAD_GLOBAL           1  'bytes'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_FALSE    53  'to 53'
               15  LOAD_CONST               ''
               18  LOAD_ATTR             2  'join'
               21  BUILD_LIST_0          0 
               24  LOAD_FAST             0  'x'
               27  GET_ITER         
               28  FOR_ITER             18  'to 49'
               31  STORE_FAST            1  'c'
               34  LOAD_GLOBAL           3  'chr'
               37  LOAD_FAST             1  'c'
               40  CALL_FUNCTION_1       1  None
               43  LIST_APPEND           2  None
               46  JUMP_BACK            28  'to 28'
               49  CALL_FUNCTION_1       1  None
               52  RETURN_VALUE_LAMBDA
             53_0  COME_FROM            12  '12'
               53  LOAD_GLOBAL           4  'str'
               56  LOAD_FAST             0  'x'
               59  CALL_FUNCTION_1       1  None
               62  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1

if PY3:
    import math
    cast_to_bin = lambda x: x if isinstance(x, bytes) else bytes([ ord(c) for c in x ])
    cast_to_chr = lambda x: ('').join([ chr(c) for c in x ])
    old_round = lambda x: float(math.floor(x + math.copysign(0.5, x)))
else:
    cast_to_bin = str
    cast_to_chr = lambda x: x
    old_round = round

def blocking_call_on_reactor_thread(func):

    def helper(*args, **kargs):
        return blockingCallFromThread(reactor, func, *args, **kargs)

    helper.__name__ = func.__name__
    return helper


def blockingCallFromThread(reactor, f, *args, **kwargs):
    """
    Improved version of twisted's blockingCallFromThread that shows the complete
    stacktrace when an exception is raised on the reactor's thread.
    If being called from the reactor thread already, just return the result of execution of the callable.
    """
    if isInIOThread():
        return f(*args, **kwargs)
    else:
        queue = Queue()

        def _callFromThread():
            result = defer.maybeDeferred(f, *args, **kwargs)
            result.addBoth(queue.put)

        reactor.callFromThread(_callFromThread)
        result = queue.get()
        if isinstance(result, Failure):
            other_thread_tb = traceback.extract_tb(result.getTracebackObject())
            this_thread_tb = traceback.extract_stack()
            logger.error('Exception raised on the reactor\'s thread %s: "%s".\n Traceback from this thread:\n%s\n Traceback from the reactor\'s thread:\n %s', result.type.__name__, result.getErrorMessage(), ('').join(traceback.format_list(this_thread_tb)), ('').join(traceback.format_list(other_thread_tb)))
            result.raiseException()
        return result


def defaultErrback(failure):
    logger.error('Deferred errback fired: %s', failure)


def addCallback(deferred, callback, errback=defaultErrback):
    """
    This global method can be used to add a callback (and optionally an errback) to a given Deferred object.
    If no errback is provided, it uses the default errback, which simply logs the failure.
    """
    return deferred.addCallbacks(callback, errback)