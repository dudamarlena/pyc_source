# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/hiro/core.py
# Compiled at: 2019-10-10 19:26:57
# Size of source mod 2**32: 14629 bytes
"""
timeline & runner implementation
"""
import copy, inspect, sys, threading, time, datetime
from six import reraise
import mock
from functools import wraps
from .errors import SegmentNotComplete, TimeOutofBounds
from .utils import timedelta_to_seconds, chained, time_in_seconds
from .patches import Date, Datetime
BLACKLIST = set()
_NO_EXCEPTION = (None, None, None)

class Decorator(object):

    def __call__(self, fn):

        @wraps(fn)
        def inner(*args, **kw):
            self.__enter__()
            exc = _NO_EXCEPTION
            try:
                if 'timeline' in inspect.getargspec(fn).args:
                    result = fn(args, timeline=self, **kw)
                else:
                    result = fn(*args, **kw)
            except Exception:
                exc = sys.exc_info()

            catch = (self.__exit__)(*exc)
            if not catch:
                if exc is not _NO_EXCEPTION:
                    reraise(*exc)
            return result

        return inner


class Segment(object):
    __doc__ = '\n    utility class to manager execution result and timings\n    for :class:`SyncRunner\n    '

    def __init__(self):
        self._Segment__error = False
        self._Segment__response = None
        self._Segment__start = time.time()
        self._Segment__end = None

    def complete(self, response):
        """
        called upon successful completion of the segment
        """
        self._Segment__response = response

    def complete_with_error(self, exception):
        """
        called if the segment errored during execution
        """
        self._Segment__error = exception

    @property
    def complete_time(self):
        """
        returns the completion time
        """
        return self._Segment__end

    @complete_time.setter
    def complete_time(self, completion_time):
        """
        sets the completion time
        """
        self._Segment__end = completion_time

    @property
    def start_time(self):
        """
        returns the start time
        """
        return self._Segment__start

    @start_time.setter
    def start_time(self, start_time):
        """
        sets the start time
        """
        self._Segment__start = start_time

    @property
    def runtime(self):
        """
        returns the total execution time of the segment
        """
        if self._Segment__end:
            return self.complete_time - self.start_time
        raise SegmentNotComplete

    @property
    def response(self):
        """
        returns the return value captured in the segment or raises
        the :exception:`exceptions.Exception` that was caught.
        """
        if not self._Segment__end:
            raise SegmentNotComplete
        else:
            if self._Segment__error:
                reraise(self._Segment__error[0], self._Segment__error[1], self._Segment__error[2])
            return self._Segment__response


class Timeline(Decorator):
    __doc__ = '\n    Timeline context manager. Within this context\n    the builtins :func:`time.time`, :func:`time.sleep`,\n    :meth:`datetime.datetime.now`, :meth:`datetime.date.today`,\n    :meth:`datetime.datetime.utcnow` and :func:`time.gmtime`\n    respect the alterations made to the timeline.\n\n    The class can be used either as a context manager or a decorator.\n\n    The following are all valid ways to use it.\n\n    .. code-block:: python\n\n        with Timeline(scale=10, start=datetime.datetime(2012,12,12)):\n            ....\n\n        fast_timeline = Timeline(scale=10).forward(120)\n\n        with fast_timeline as timeline:\n            ....\n\n        delta = datetime.date(2015,1,1) - datetime.date.today()\n        future_frozen_timeline = Timeline(scale=10000).freeze().forward(delta)\n        with future_frozen_timeline as timeline:\n            ...\n\n        @Timeline(scale=100)\n        def slow():\n            time.sleep(120)\n\n\n    :param float scale: > 1 time will go faster and < 1 it will be slowed down.\n    :param start: if specified starts the timeline at the given value (either a\n        floating point representing seconds since epoch or a\n        :class:`datetime.datetime` object)\n\n    '
    class_mappings = {'date':(
      datetime.date, Date), 
     'datetime':(
      datetime.datetime, Datetime)}

    def __init__(self, scale=1, start=None):
        self.reference = time.time()
        self.offset = time_in_seconds(start) - self.reference if start else 0.0
        self.freeze_point = self.freeze_at = None
        self.patchers = []
        self.mock_mappings = {'datetime.date':(
          datetime.date, Date), 
         'datetime.datetime':(
          datetime.datetime, Datetime), 
         'time.time':(
          time.time, self._Timeline__time_time), 
         'time.sleep':(
          time.sleep, self._Timeline__time_sleep), 
         'time.gmtime':(
          time.gmtime, self._Timeline__time_gmtime)}
        self.func_mappings = {'time':(
          time.time, self._Timeline__time_time), 
         'sleep':(
          time.sleep, self._Timeline__time_sleep), 
         'gmtime':(
          time.gmtime, self._Timeline__time_gmtime)}
        self.factor = scale

    def _get_original(self, fn_or_mod):
        """
        returns the original moduel or function
        """
        if fn_or_mod in self.mock_mappings:
            return self.mock_mappings[fn_or_mod][0]
        if fn_or_mod in self.func_mappings:
            return self.func_mappings[fn_or_mod][0]
        return self.class_mappings[fn_or_mod][0]

    def _get_fake(self, fn_or_mod):
        """
        returns the mocked/patched module or function
        """
        if fn_or_mod in self.mock_mappings:
            return self.mock_mappings[fn_or_mod][1]
        if fn_or_mod in self.func_mappings:
            return self.func_mappings[fn_or_mod][1]
        return self.class_mappings[fn_or_mod][1]

    def __compute_time(self, freeze_point, offset):
        """
        computes the current_time after accounting for
        any adjustments due to :attr:`factor` or invocations
        of :meth:`freeze`, :meth:`rewind` or :meth:`forward`
        """
        if freeze_point is not None:
            return offset + freeze_point
        delta = self._get_original('time.time')() - self.reference
        return self.reference + delta * self.factor + offset

    def __check_out_of_bounds(self, offset=None, freeze_point=None):
        """
        ensures that the time that would be calculated based on any
        offset or freeze point would not result in jumping beyond the epoch
        """
        next_time = self._Timeline__compute_time(freeze_point or self.freeze_point, offset or self.offset)
        if next_time < 0:
            raise TimeOutofBounds(next_time)

    def __time_time(self):
        """
        patched version of :func:`time.time`
        """
        return self._Timeline__compute_time(self.freeze_point, self.offset)

    def __time_gmtime(self, seconds=None):
        """
        patched version of :func:`time.gmtime`
        """
        return self._get_original('time.gmtime')(seconds or self._Timeline__time_time())

    def __time_sleep(self, amount):
        """
        patched version of :func:`time.sleep`
        """
        self._get_original('time.sleep')(1.0 * amount / self.factor)

    @chained
    def forward(self, amount):
        """
        forwards the timeline by the specified :attr:`amount`

        :param amount: either an integer representing seconds or
         a :class:`datetime.timedelta` object
        """
        offset = self.offset
        if isinstance(amount, datetime.timedelta):
            offset += timedelta_to_seconds(amount)
        else:
            offset += amount
        self._Timeline__check_out_of_bounds(offset=offset)
        self.offset = offset

    @chained
    def rewind(self, amount):
        """
        rewinds the timeline by the specified :attr:`amount`

        :param amount: either an integer representing seconds or
         a :class:`datetime.timedelta` object
        """
        offset = self.offset
        if isinstance(amount, datetime.timedelta):
            offset -= timedelta_to_seconds(amount)
        else:
            offset -= amount
        self._Timeline__check_out_of_bounds(offset=offset)
        self.offset = offset

    @chained
    def freeze(self, target_time=None):
        """
        freezes the timeline

        :param target_time: the time to freeze at as either a float representing
            seconds since the epoch or a :class:`datetime.datetime` object.
            If not provided time will be frozen at the current time of the
            enclosing :class:`Timeline`
        """
        if target_time is None:
            freeze_point = self._get_fake('time.time')()
        else:
            freeze_point = time_in_seconds(target_time)
        self._Timeline__check_out_of_bounds(freeze_point=freeze_point)
        self.freeze_point = freeze_point
        self.offset = 0

    @chained
    def unfreeze(self):
        """
        if a call to :meth:`freeze` was previously made, the timeline will be
        unfrozen to the point which :meth:`freeze` was invoked.

        .. warning::

            Since unfreezing will reset the timeline back to the point in
            when the :meth:`freeze` was invoked - the effect of previous
            invocations of :meth:`forward` and :meth:`rewind` will
            be lost. This is by design so that freeze/unfreeze can be used as
            a checkpoint mechanism.

        """
        if self.freeze_point is not None:
            self.reference = self._get_original('time.time')()
            self.offset = time_in_seconds(self.freeze_point) - self.reference
            self.freeze_point = None

    @chained
    def scale(self, factor):
        """
        changes the speed at which time elapses and how long sleeps last for.

        :param float factor: > 1 time will go faster and < 1 it will be slowed
            down.

        """
        self.factor = factor
        self.reference = self._get_original('time.time')()

    @chained
    def reset(self):
        """
        resets the current timeline to the actual time now
        with a scale factor 1
        """
        self.factor = 1
        self.freeze_point = None
        self.reference = self._get_original('time.time')()
        self.offset = 0

    def __enter__(self):
        for name in list(sys.modules.keys()):
            module = sys.modules[name]
            if module in BLACKLIST:
                continue
            mappings = copy.copy(self.class_mappings)
            mappings.update(self.func_mappings)
            for obj in mappings:
                try:
                    if obj in dir(module):
                        if getattr(module, obj) == self._get_original(obj):
                            path = '%s.%s' % (name, obj)
                            if path not in self.mock_mappings:
                                patcher = mock.patch(path, self._get_fake(obj))
                                patcher.start()
                                self.patchers.append(patcher)
                except:
                    BLACKLIST.add(module)

        for time_obj in self.mock_mappings:
            patcher = mock.patch(time_obj, self._get_fake(time_obj))
            patcher.start()
            self.patchers.append(patcher)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for patcher in self.patchers:
            patcher.stop()

        self.patchers = []


class ScaledRunner(object):
    __doc__ = '\n    manages the execution of a callable within a :class:`hiro.Timeline`\n    context.\n    '

    def __init__(self, factor, func, *args, **kwargs):
        self.func = func
        self.func_args = args
        self.func_kwargs = kwargs
        self.segment = Segment()
        self.factor = factor
        self.__call__()

    def _run(self):
        """
        managed execution of :attr:`func`
        """
        self.segment.start_time = time.time()
        with Timeline(scale=(self.factor)):
            try:
                self.segment.complete((self.func)(*self.func_args, **self.func_kwargs))
            except:
                self.segment.complete_with_error(sys.exc_info())

        self.segment.complete_time = time.time()

    def __call__(self):
        self._run()
        return self

    def get_response(self):
        """
        :returns: the return value from :attr:`func`
        :raises: Exception if the :attr:`func` raised one during execution
        """
        return self.segment.response

    def get_execution_time(self):
        """
        :returns: the real execution time of :attr:`func` in seconds
        """
        return self.segment.runtime


class ScaledAsyncRunner(ScaledRunner):
    __doc__ = '\n    manages the asynchronous execution of a callable within a\n    :class:`hiro.Timeline` context.\n    '

    def __init__(self, *args, **kwargs):
        self.thread_runner = threading.Thread(target=(self._run))
        (super(ScaledAsyncRunner, self).__init__)(*args, **kwargs)

    def __call__(self):
        self.thread_runner.start()
        return self

    def is_running(self):
        """
        :rtype bool: whether the :attr:`func` is still running or not.
        """
        return self.thread_runner.is_alive()

    def join(self):
        """
        waits for the :attr:`func` to complete execution.
        """
        return self.thread_runner.join()


def run_sync(factor, func, *args, **kwargs):
    """
    Executes a callable within a :class:`hiro.Timeline`

    :param int factor: scale factor to use for the timeline during execution
    :param function func: the function to invoke
    :param args: the arguments to pass to the function
    :param kwargs: the keyword arguments to pass to the function
    :returns: an instance of :class:`hiro.core.ScaledRunner`

    """
    return ScaledRunner(factor, func, *args, **kwargs)


def run_async(factor, func, *args, **kwargs):
    """
    Asynchronously executes a callable within a :class:`hiro.Timeline`

    :param int factor: scale factor to use for the timeline during execution
    :param function func: the function to invoke
    :param args: the arguments to pass to the function
    :param kwargs: the keyword arguments to pass to the function
    :returns: an instance of :class:`hiro.core.ScaledAsyncRunner`

    """
    return ScaledAsyncRunner(factor, func, *args, **kwargs)