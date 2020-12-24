# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wursterk/code/tinyflow/venv/lib/python3.6/site-packages/tinyflow/pipeline.py
# Compiled at: 2017-03-15 21:10:24
# Size of source mod 2**32: 2016 bytes
"""Pipeline model."""
from .exceptions import NoPool, NotAnOperation
from .ops import Operation

class Pipeline(object):
    __doc__ = 'A ``tinyflow`` pipeline model.'

    def __init__(self):
        self.transforms = []
        self._thread_pool = None
        self._process_pool = None

    @property
    def thread_pool(self):
        if self._thread_pool is None:
            raise NoPool('An operation requested a thread pool but {!r} did not receive one.'.format(self))
        return self._thread_pool

    @property
    def process_pool(self):
        if self._process_pool is None:
            raise NoPool('An operation requested a process pool but {!r} did not receive one.'.format(self))
        return self._process_pool

    def __or__(self, other):
        """Add a transform to the pipeline."""
        if not isinstance(other, Operation):
            raise NotAnOperation("Expected an 'Operation()', not: {}".format(other))
        other.pipeline = self
        self.transforms.append(other)
        return self

    __ior__ = __or__

    def __call__(self, data, process_pool=None, thread_pool=None):
        """Stream data through the pipeline.

        Parameters
        ----------
        data : object
            Input data.  Most operations expect an iterable, but some
            do not.
        process_pool : None or concurrent.futures.ProcessPoolExecutor
            A process pool that individual operations can use if needed.
        thread_pool : None or concurrent.futures.ThreadPoolExecutor
            A thread pool that individual operations can use if needed.
        """
        self._process_pool = process_pool
        self._thread_pool = thread_pool
        for trans in self.transforms:
            data = trans(data)

        return data