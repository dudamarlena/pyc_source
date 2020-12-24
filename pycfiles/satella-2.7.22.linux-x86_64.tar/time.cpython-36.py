# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/time.py
# Compiled at: 2020-05-04 17:22:35
# Size of source mod 2**32: 2961 bytes
import typing as tp, time
from concurrent.futures import Future
from functools import wraps
__all__ = [
 'measure']

class measure:
    __doc__ = "\n    A class used to measure time elapsed. Use for example like this:\n\n    >>> with measure() as measurement:\n    >>>     time.sleep(1)\n    >>>     print('This has taken so far', measurement(), 'seconds')\n    >>>     time.sleep(1)\n    >>> print('A total of ', measurement(), 'seconds have elapsed')\n\n    You can also use the .start() method instead of context manager. Time measurement\n    will stop after exiting or calling .stop() depending on stop_on_stop flag.\n\n    You can also decorate your functions to have them keep track time of their execution, like that:\n\n    >>> @measure()\n    >>> def measuring(measurement_object: measure, *args, **kwargs):\n    >>>     ...\n\n    You can also measure how long does executing a future take, eg.\n\n    >>> future = get_my_future()\n    >>> measurement = measure(future)\n    >>> future.result()\n    >>> print('Executing the future took', measurement(), 'seconds')\n\n    In case a future is passed, the measurement will stop automatically as soon as the future\n    returns with a result (or exception)\n\n    :param stop_on_stop: stop elapsing time upon calling .stop()/exiting the context manager\n    :param adjust: interval to add to current time upon initialization\n    "
    __slots__ = ('started_on', 'elapsed', 'stopped_on', 'stop_on_stop')

    def __init__(self, future_to_measure: tp.Optional[Future]=None, stop_on_stop: bool=True, adjust: float=0.0):
        self.started_on = time.monotonic() + adjust
        self.elapsed = None
        self.stopped_on = None
        self.stop_on_stop = stop_on_stop
        if future_to_measure is not None:
            future_to_measure.add_done_callback(lambda fut: self.stop())

    def start(self) -> None:
        """Start measuring time or update the internal counter"""
        self.started_on = time.monotonic()

    def update(self) -> None:
        """Alias for .start()"""
        self.start()

    def adjust(self, interval: float) -> None:
        """Add given value to internal started_at counter"""
        self.started_on += interval

    def __call__(self, fun: tp.Optional[tp.Callable]=None) -> float:
        if fun is None:
            if self.stop_on_stop:
                if self.elapsed is not None:
                    return self.elapsed
            return time.monotonic() - self.started_on
        else:

            @wraps(fun)
            def inner(*args, **kwargs):
                with self:
                    return fun(self, *args, **kwargs)

            return inner

    def __enter__(self):
        self.start()
        return self

    def stop(self) -> None:
        """Stop counting time"""
        self.stopped_on = time.monotonic()
        self.elapsed = self.stopped_on - self.started_on

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False