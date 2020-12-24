# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/framework/foundation/stream_util.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 4772 bytes
"""Helpful utilities related to the stream module."""
import logging, threading
from grpc.framework.foundation import stream
_NO_VALUE = object()
_LOGGER = logging.getLogger(__name__)

class TransformingConsumer(stream.Consumer):
    __doc__ = 'A stream.Consumer that passes a transformation of its input to another.'

    def __init__(self, transformation, downstream):
        self._transformation = transformation
        self._downstream = downstream

    def consume(self, value):
        self._downstream.consume(self._transformation(value))

    def terminate(self):
        self._downstream.terminate()

    def consume_and_terminate(self, value):
        self._downstream.consume_and_terminate(self._transformation(value))


class IterableConsumer(stream.Consumer):
    __doc__ = 'A Consumer that when iterated over emits the values it has consumed.'

    def __init__(self):
        self._condition = threading.Condition()
        self._values = []
        self._active = True

    def consume(self, value):
        with self._condition:
            if self._active:
                self._values.append(value)
                self._condition.notify()

    def terminate(self):
        with self._condition:
            self._active = False
            self._condition.notify()

    def consume_and_terminate(self, value):
        with self._condition:
            if self._active:
                self._values.append(value)
                self._active = False
                self._condition.notify()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        with self._condition:
            while self._active and not self._values:
                self._condition.wait()

            if self._values:
                return self._values.pop(0)
            raise StopIteration()


class ThreadSwitchingConsumer(stream.Consumer):
    __doc__ = 'A Consumer decorator that affords serialization and asynchrony.'

    def __init__(self, sink, pool):
        self._lock = threading.Lock()
        self._sink = sink
        self._pool = pool
        self._spinning = False
        self._values = []
        self._active = True

    def _spin(self, sink, value, terminate):
        while True:
            try:
                if value is _NO_VALUE:
                    sink.terminate()
                else:
                    if terminate:
                        sink.consume_and_terminate(value)
                    else:
                        sink.consume(value)
            except Exception as e:
                _LOGGER.exception(e)

            with self._lock:
                if terminate:
                    self._spinning = False
                    return
                else:
                    if self._values:
                        value = self._values.pop(0)
                        terminate = not self._values and not self._active
                    else:
                        if not self._active:
                            value = _NO_VALUE
                            terminate = True
                        else:
                            self._spinning = False
                            return

    def consume(self, value):
        with self._lock:
            if self._active:
                if self._spinning:
                    self._values.append(value)
                else:
                    self._pool.submit(self._spin, self._sink, value, False)
                    self._spinning = True

    def terminate(self):
        with self._lock:
            if self._active:
                self._active = False
                if not self._spinning:
                    self._pool.submit(self._spin, self._sink, _NO_VALUE, True)
                    self._spinning = True

    def consume_and_terminate(self, value):
        with self._lock:
            if self._active:
                self._active = False
                if self._spinning:
                    self._values.append(value)
                else:
                    self._pool.submit(self._spin, self._sink, value, True)
                    self._spinning = True