# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyppeteer/pyppeteer/helper.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 5414 bytes
"""Helper functions."""
import asyncio, json, logging, math
from typing import Any, Awaitable, Callable, Dict, List
from pyee import EventEmitter
import pyppeteer
from pyppeteer.connection import CDPSession
from pyppeteer.errors import ElementHandleError, TimeoutError
logger = logging.getLogger(__name__)

def debugError(_logger: logging.Logger, msg: Any) -> None:
    """Log error messages."""
    if pyppeteer.DEBUG:
        _logger.error(msg)
    else:
        _logger.debug(msg)


def evaluationString(fun: str, *args: Any) -> str:
    """Convert function and arguments to str."""
    _args = ', '.join([json.dumps('undefined' if arg is None else arg) for arg in args])
    expr = f"({fun})({_args})"
    return expr


def getExceptionMessage(exceptionDetails: dict) -> str:
    """Get exception message from `exceptionDetails` object."""
    exception = exceptionDetails.get('exception')
    if exception:
        return exception.get('description') or exception.get('value')
    message = exceptionDetails.get('text', '')
    stackTrace = exceptionDetails.get('stackTrace', dict())
    if stackTrace:
        for callframe in stackTrace.get('callFrames'):
            location = str(callframe.get('url', '')) + ':' + str(callframe.get('lineNumber', '')) + ':' + str(callframe.get('columnNumber'))
            functionName = callframe.get('functionName', '<anonymous>')
            message = message + f"\n    at {functionName} ({location})"

    return message


def addEventListener(emitter: EventEmitter, eventName: str, handler: Callable) -> Dict[(str, Any)]:
    """Add handler to the emitter and return emitter/handler."""
    emitter.on(eventName, handler)
    return {'emitter':emitter,  'eventName':eventName,  'handler':handler}


def removeEventListeners(listeners: List[dict]) -> None:
    """Remove listeners from emitter."""
    for listener in listeners:
        emitter = listener['emitter']
        eventName = listener['eventName']
        handler = listener['handler']
        emitter.remove_listener(eventName, handler)

    listeners.clear()


unserializableValueMap = {'-0':0, 
 'NaN':None, 
 None:None, 
 'Infinity':math.inf, 
 '-Infinity':-math.inf}

def valueFromRemoteObject(remoteObject: Dict) -> Any:
    """Serialize value of remote object."""
    if remoteObject.get('objectId'):
        raise ElementHandleError('Cannot extract value when objectId is given')
    value = remoteObject.get('unserializableValue')
    if value:
        if value == '-0':
            return 0
        if value == 'NaN':
            return
        if value == 'Infinity':
            return math.inf
        if value == '-Infinity':
            return -math.inf
        raise ElementHandleError('Unsupported unserializable value: {}'.format(value))
    return remoteObject.get('value')


def releaseObject(client: CDPSession, remoteObject: dict) -> Awaitable:
    """Release remote object."""
    objectId = remoteObject.get('objectId')
    fut_none = client._loop.create_future()
    fut_none.set_result(None)
    if not objectId:
        return fut_none
    try:
        return client.send('Runtime.releaseObject', {'objectId': objectId})
    except Exception as e:
        try:
            debugError(logger, e)
        finally:
            e = None
            del e

    return fut_none


def waitForEvent(emitter: EventEmitter, eventName: str, predicate: Callable[([Any], bool)], timeout: float, loop: asyncio.AbstractEventLoop) -> Awaitable:
    """Wait for an event emitted from the emitter."""
    promise = loop.create_future()

    def resolveCallback(target):
        promise.set_result(target)

    def rejectCallback(exception):
        promise.set_exception(exception)

    async def timeoutTimer():
        await asyncio.sleep(timeout / 1000)
        rejectCallback(TimeoutError('Timeout exceeded while waiting for event'))

    def _listener(target):
        if not predicate(target):
            return
        cleanup()
        resolveCallback(target)

    listener = addEventListener(emitter, eventName, _listener)
    if timeout:
        eventTimeout = loop.create_task(timeoutTimer())

    def cleanup():
        removeEventListeners([listener])
        if timeout:
            eventTimeout.cancel()

    return promise


def get_positive_int(obj: dict, name: str) -> int:
    """Get and check the value of name in obj is positive integer."""
    value = obj[name]
    if not isinstance(value, int):
        raise TypeError(f"{name} must be integer: {type(value)}")
    else:
        if value < 0:
            raise ValueError(f"{name} must be positive integer: {value}")
    return value


def is_jsfunc(func: str) -> bool:
    """Heuristically check function or expression."""
    func = func.strip()
    if func.startswith('function') or func.startswith('async '):
        return True
    if '=>' in func:
        return True
    return False