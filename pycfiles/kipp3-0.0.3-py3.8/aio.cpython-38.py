# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/libs/aio.py
# Compiled at: 2019-11-08 04:26:21
# Size of source mod 2**32: 4330 bytes
"""
---------------------------
Asynchronous Base Interface
---------------------------

There's no need to use this module directly, you can use ``kipp.aio``
"""
from __future__ import unicode_literals
from threading import RLock
from datetime import timedelta
import tornado
from tornado.concurrent import run_on_executor
from tornado.gen import coroutine, sleep, multi, Future, Return, TimeoutError
from tornado.locks import Semaphore, Event as ToroEvent, Condition
import tornado.queues as Tornado_Queue
from .exceptions import KippAIOException, KippAIOTimeoutError

def return_in_coroutine(ret):
    """Return value in a coroutine"""
    raise tornado.gen.Return(ret)


class Event(ToroEvent):

    @coroutine
    def wait(self, timeout=None):
        """
        Args:
            timeout (int, default=None): seconds to wait for
        """
        try:
            timeout = timeout and timedelta(seconds=timeout)
            r = yield super(Event, self).wait(timeout=timeout)
        except TimeoutError as err:
            try:
                raise KippAIOTimeoutError(err)
            finally:
                err = None
                del err

        else:
            return_in_coroutine(r)

    def __getattr__(self, name):
        return super(Event, self).__getattr__(name)


class Queue(Tornado_Queue):

    def empty(self):
        return self.qsize() == 0


class MultiEvent(Event):
    __doc__ = 'Event for multi workers\n\n    Examples:\n    ::\n        from kipp.aio import MultiEvent\n\n        evt = MultiEvent(3)\n\n        evt.set()\n        evt.is_set()  # False\n        evt.set()\n        evt.is_set()  # False\n        evt.set()\n        evt.is_set()  # True\n    '

    def __init__(self, n_workers=1):
        """
        Args:
            n_workers (int, default=1): how many workers will receive this event
        """
        try:
            assert isinstance(n_workers, int), 'MultiEvent(n_workers) should be integer'
            assert n_workers >= 1, 'MultiEvent(n_workers) should greater than 1'
        except AssertionError as err:
            try:
                raise KippAIOException(err)
            finally:
                err = None
                del err

        else:
            self._MultiEvent__lock = RLock()
            self._MultiEvent__n_event = n_workers
            super(MultiEvent, self).__init__()

    def set--- This code section failed: ---

 L.  87         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _MultiEvent__lock
                4  SETUP_WITH           62  'to 62'
                6  POP_TOP          

 L.  88         8  LOAD_FAST                'self'
               10  DUP_TOP          
               12  LOAD_ATTR                _MultiEvent__n_event
               14  LOAD_CONST               1
               16  INPLACE_SUBTRACT 
               18  ROT_TWO          
               20  STORE_ATTR               _MultiEvent__n_event

 L.  89        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _MultiEvent__n_event
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    58  'to 58'

 L.  90        32  LOAD_GLOBAL              super
               34  LOAD_GLOBAL              MultiEvent
               36  LOAD_FAST                'self'
               38  CALL_FUNCTION_2       2  ''
               40  LOAD_METHOD              set
               42  CALL_METHOD_0         0  ''
               44  POP_BLOCK        
               46  ROT_TWO          
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  RETURN_VALUE     
             58_0  COME_FROM            30  '30'
               58  POP_BLOCK        
               60  BEGIN_FINALLY    
             62_0  COME_FROM_WITH        4  '4'
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 46


def _get_event_loop():
    return tornado.ioloop.IOLoop()


ioloop = _get_event_loop()

def wait(futures):
    """Gather multiply futures into one future

    Returns:
        future: New future wait all child futures
            the result is a list contains the results of all child futures
    """
    return multi(set(futures))


def as_completed(futures, timeout=None):
    """Wait for futures until any future is done

    Args:
        futures (list): consists of futures
        timeout (int): max seconds to waiting for each future

    Examples:
    ::
        from kipp.aio import coroutine2, sleep, as_completed

        @coroutine2
        def wait_for_seconds(sec):
            yield sleep(sec)

        futures = [
            wait_for_seconds(2),
            wait_for_seconds(1),
        ]

        for future in as_completed(futures):
            result = future.result()
            print(result)
            # >> 1
            # >> 2
    """
    futures = set(futures)
    _completed = []
    _lock = RLock()
    evt = Event()

    def _set_evt(futu):
        with _lock:
            evt.set()
            _completed.append(futu)

    for futu in futures:
        futu.add_done_callback(_set_evt)
    else:
        while not all([futu.done() for futu in futures]):
            f_evt = evt.wait(timeout=timeout)
            run_until_complete(f_evt)
            f_evt.result()
            with _lock:
                while _completed:
                    (yield _completed.pop(0))

                evt.clear()


def get_event_loop():
    """Get current ioloop"""
    return ioloop


def _stop(future):
    ioloop.stop()


def run_until_complete(future, ioloop=ioloop):
    """Keep running untill the future is done"""
    ioloop.add_future(future, _stop)
    ioloop.start()


if __name__ == '__main__':

    @coroutine
    def demo():
        (yield sleep(1))
        print('ok')
        return_in_coroutine(2)


    future = demo()
    run_until_complete(future)
    print('result:', future.result())