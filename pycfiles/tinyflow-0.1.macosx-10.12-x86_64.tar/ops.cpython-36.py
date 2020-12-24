# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wursterk/code/tinyflow/venv/lib/python3.6/site-packages/tinyflow/ops.py
# Compiled at: 2017-03-15 21:10:24
# Size of source mod 2**32: 13173 bytes
"""Pipeline operations for processing data serially."""
import abc
from collections import Counter, deque
import copy
from functools import reduce
import itertools as it
from . import _compat, tools
from .exceptions import NoPipeline
__all__ = [
 'Operation', 'map', 'wrap', 'sort', 'filter',
 'flattentake', 'drop', 'windowed_op',
 'windowed_reduce', 'counter', 'reduce_by_key']

class Operation(object):
    __doc__ = 'Base class for developing pipeline steps.'

    @property
    def description(self):
        """A transform description can be added like:

            Pipeline() | "description" >> Operation()
        """
        return getattr(self, '_description', repr(self))

    @description.setter
    def description(self, value):
        """Subclassers use ``__init__()`` for arguments.  This is good
        enough.
        """
        self._description = value

    @property
    def pipeline(self):
        """Operation's parent pipeline."""
        pipeline = getattr(self, '_pipeline', None)
        if pipeline is None:
            raise NoPipeline('Operation {} not attached to a pipeline.'.format(repr(self)))
        else:
            return pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        self._pipeline = pipeline

    @abc.abstractmethod
    def __call__(self, stream):
        """Given a stream of data, apply the transform.

        Parameters
        ----------
        stream : iter
            Apply transform to the stream of data.

        Yields
        ------
        object
            Operationed objects.
        """
        raise NotImplementedError

    def __rrshift__(self, other):
        """Add a description to this pipeline phase."""
        self.description = other
        return self


class map(Operation):
    __doc__ = 'Map a function across the stream of data.'

    def __init__(self, func, argtype='single', flatten=False, pool=None):
        """
        Parameters
        ----------
        func : function
            Map this function.
        argtype : str, optional
            Determines how items from the stream are passed to ``func``.
                single: Like ``map(func, stream)``.
                *args**kwargs: Like ``map(lambda x: func(*x[0], **x[1]), stream)``.
                *args: Like ``itertools.starmap(func, stream)``.
                **kwargs: Like ``map(lambda x: func(**x), stream)``
        flatten : bool, optional
            Like: ``itertools.chain.from_iterable(map(<func>, <iterable>))``.
        pool : str, optional
            Use 'thread' for thread pool or 'process' for process pool.
            The corresponding pool must be passed to ``Pipeline.__call__()``
            at the time of computation.
        """
        self.func = func
        self.flatten = flatten
        self.queue = deque()
        self.argtype = argtype
        self._compute_no_pool([])
        self.pool = pool
        self.worker_pool = None

    def flush_queue(self, count=None):
        queue = self.queue
        append = queue.append
        popleft = queue.popleft
        i = 0
        while queue:
            item = popleft()
            if item.done():
                yield item.result()
            else:
                append(item)
            i += 1
            if count is not None:
                if i > count:
                    break

    def _compute_no_pool(self, stream):
        if self.argtype == 'single':
            return _compat.map(self.func, stream)
        else:
            if self.argtype == '*args':
                return it.starmap(self.func, stream)
            if self.argtype == '**kwargs':
                return _compat.map(lambda x: (self.func)(**x), stream)
            if self.argtype == '*args**kwargs':
                return it.starmap(lambda args, kwargs: (self.func)(*args, **kwargs), stream)
        raise ValueError('Invalid argtype: {}'.format(self.argtype))

    def _compute_with_pool(self, stream):
        queue = self.queue
        pool = self.worker_pool
        for idx, item in enumerate(stream, 1):
            if self.argtype == 'single':
                future = pool.submit(self.func, item)
            else:
                if self.argtype == '*args':
                    future = (pool.submit)(self.func, *item)
                else:
                    if self.argtype == '**kwargs':
                        future = (pool.submit)(
                         (self.func), **item)
                    else:
                        if self.argtype == '*args**kwargs':
                            future = (pool.submit)(
 self.func, *(item[0]), **item[1])
                        else:
                            raise ValueError('Invalid argtype: {}'.format(self.argtype))
            queue.append(future)
            if idx % 10 == 0:
                for out in self.flush_queue(len(queue)):
                    yield out

        for item in self.flush_queue():
            yield item

    def __call__(self, stream):
        if self.pool is None:
            pass
        else:
            if self.pool == 'thread':
                self.worker_pool = self.pipeline.thread_pool
            else:
                if self.pool == 'process':
                    self.worker_pool = self.pipeline.process_pool
                else:
                    raise ValueError('Invalid pool: {}'.format(self.pool))
                if self.worker_pool:
                    results = self._compute_with_pool(stream)
                else:
                    results = self._compute_no_pool(stream)
            if self.flatten:
                results = it.chain.from_iterable(results)
            return results


class wrap(Operation):
    __doc__ = 'Wrap the data stream in an arbitrary transform.\n\n    For example:\n\n        Pipeline() | ops.wrap(itertools.chain.from_iterable)\n\n    produces the same result as:\n\n        Pipeline() | ops.flatten()\n    '

    def __init__(self, func):
        """
        Parameters
        ----------
        func : function
            Wrap the data stream with this function.
        """
        self.func = func

    def __call__(self, stream):
        return self.func(stream)


class sort(Operation):
    __doc__ = 'Sort the stream of data.  Just a wrapper around ``sorted()``.'

    def __init__(self, key=None, reverse=False):
        """
        Parameters
        ----------
        key : callable or None, optional
            Key function for ``sorted()``.
        reverse : bool, optional
            For ``sorted()``.
        """
        self.key = key
        self.reverse = reverse

    def __call__(self, stream):
        return sorted(stream, key=(self.key), reverse=(self.reverse))


class filter(Operation):
    __doc__ = 'Filter the data stream.  Keeps elements that evaluate as ``True``.'

    def __init__(self, func):
        """
        Parameters
        ----------
        func : function
            See ``filtered()``'s documentation.
        """
        self.func = func

    def __call__(self, stream):
        return _compat.filter(self.func, stream)


class flatten(Operation):
    __doc__ = 'Flatten an iterable.  Like ``itertools.chain.from_iterable()``.'

    def __call__(self, stream):
        return it.chain.from_iterable(stream)


class take(Operation):
    __doc__ = 'Take N items from the stream.'

    def __init__(self, count):
        """
        Parameters
        ----------
        count : int
            Take this many items.
        """
        self.count = count

    def __call__(self, stream):
        return it.islice(stream, self.count)


class drop(Operation):
    __doc__ = 'Drop N items from the stream.'

    def __init__(self, count):
        """
        Parameters
        ----------
        count : int
            Drop this many items.
        """
        self.count = count

    def __call__(self, stream):
        stream = iter(stream)
        for _ in range(self.count):
            next(stream)

        return stream


class windowed_op(Operation):
    __doc__ = 'Windowed operations.  Group ``count`` items and hand off to\n    ``operation``.  Items are yielded from ``operation`` individually\n    back into the stream.\n    '

    def __init__(self, count, operation):
        """
        Parameters
        ----------
        count : int
            Apply ``operation`` across a group of ``count`` items.
        operation : callable
            Apply this function to groups of items.
        """
        self.count = count
        self.operation = operation

    def __call__(self, stream):
        windows = tools.slicer(stream, self.count)
        results = _compat.map(self.operation, windows)
        return it.chain.from_iterable(results)


class windowed_reduce(Operation):
    __doc__ = 'Group N items together into a window and reduce to a single value.'

    def __init__(self, count, reducer):
        """
        Parameters
        ----------
        count : int
            Window size.
        reducer : function
            Like ``operator.iadd()``.
        """
        self.count = count
        self.reducer = reducer

    def __call__(self, stream):
        for window in tools.slicer(stream, self.count):
            yield reduce(self.reducer, window)


class counter(Operation):
    __doc__ = 'Count items and optionally produce only the N most common.'

    def __init__(self, most_common=None):
        """
        Parameters
        ----------
        most_common : int or None, optional
            Only emit the N most common items.
        """
        self.most_common = most_common

    def __call__(self, stream):
        frequency = Counter(stream)
        if self.most_common:
            results = frequency.most_common(self.most_common)
        else:
            results = frequency.items()
        return iter(results)


class reduce_by_key(Operation):
    __doc__ = 'Apply a reducer by key.  Holds all keys plus one value for each key\n    in memory until items are emitted.\n\n    Given a stream of words this would produce a sequence of\n    ``(word, frequency)`` tuples:\n\n        import operator\n\n        reduce_by_key(\n            operator.iadd,\n            keyfunc=lambda x: x,\n            valfunc=lambda x: 1)\n\n    Values are emitted as a sequence of ``(key, val)`` tuples.\n    '

    def __init__(self, reducer, keyfunc, valfunc=lambda x: x, initial=tools.NULL, copy_initial=False, deepcopy_initial=False):
        """
        Parameters
        ----------
        reducer : callable
            Function for reducing values.  Must take two values and return
            one, like ``operator.iadd()`` or: ``lambda a, b: a + b``.
        keyfunc : callable
            Function for extracting the key from every input item.
        valfunc : callable, optional
            Function for extracting the value from every input item.  If not
            given the item itself is used as the value.
        initial : object, optional
            Reduce the first value for each key against this initial value,
            like the ``initial`` parameter for ``functools.reduce()`` but
            ``None`` is valid.
        copy_initial : bool, optional
            Pass ``initial`` through ``copy.copy()`` before use.
            Prevents mutable objects from being altered by every key at the
            cost of some overhead.  Cannot be combined with
            ``deepcopy_initial``.
        deepcopy_initial : bool, optional
            Same as ``copy_initial`` but with ``copy.deepcopy()``.  Cannot
            be combined with ``copy_initial``.
        """
        self.reducer = reducer
        self.keyfunc = keyfunc
        self.valfunc = valfunc
        self.initial = initial
        self.copy_initial = copy_initial
        if copy_initial:
            if deepcopy_initial:
                raise ValueError("Cannot combine 'copy_initial' and 'deepcopy_initial'.")
        else:
            if copy_initial:
                self.copier = copy.copy
            else:
                if deepcopy_initial:
                    self.copier = copy.deepcopy
                else:
                    self.copier = lambda x: x

    def __call__(self, stream):
        partitioned = {}
        stream = ((self.keyfunc(i), self.valfunc(i)) for i in stream)
        for key, value in stream:
            p_value = partitioned.get(key, tools.NULL)
            if p_value != tools.NULL:
                partitioned[key] = self.reducer(p_value, value)
            else:
                if p_value == tools.NULL:
                    if self.initial == tools.NULL:
                        partitioned[key] = value
                if self.initial != tools.NULL:
                    partitioned[key] = self.reducer(self.copier(self.initial), value)
                else:
                    raise ValueError("This shouldn't happen.")

        while partitioned:
            yield partitioned.popitem()