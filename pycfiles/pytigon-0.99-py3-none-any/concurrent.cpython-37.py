# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/contrib/concurrent.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 3772 bytes
"""
Thin wrappers around `concurrent.futures`.
"""
from __future__ import absolute_import
from tqdm import TqdmWarning
import tqdm.auto as tqdm_auto
from copy import deepcopy
try:
    from operator import length_hint
except ImportError:

    def length_hint(it, default=0):
        """Returns `len(it)`, falling back to `default`"""
        try:
            return len(it)
        except TypeError:
            return default


try:
    from os import cpu_count
except ImportError:
    try:
        from multiprocessing import cpu_count
    except ImportError:

        def cpu_count():
            return 4


import sys
__author__ = {'github.com/': ['casperdcl']}
__all__ = ['thread_map', 'process_map']

def _executor_map(PoolExecutor, fn, *iterables, **tqdm_kwargs):
    """
    Implementation of `thread_map` and `process_map`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    max_workers  : [default: max(32, cpu_count() + 4)].
    chunksize  : [default: 1].
    """
    kwargs = deepcopy(tqdm_kwargs)
    if 'total' not in kwargs:
        kwargs['total'] = len(iterables[0])
    tqdm_class = kwargs.pop('tqdm_class', tqdm_auto)
    max_workers = kwargs.pop('max_workers', min(32, cpu_count() + 4))
    chunksize = kwargs.pop('chunksize', 1)
    pool_kwargs = dict(max_workers=max_workers)
    sys_version = sys.version_info[:2]
    if sys_version >= (3, 7):
        pool_kwargs.update(initializer=(tqdm_class.set_lock),
          initargs=(tqdm_class.get_lock(),))
    map_args = {}
    if not (3, 0) < sys_version < (3, 5):
        map_args.update(chunksize=chunksize)
    with PoolExecutor(**pool_kwargs) as (ex):
        return list(tqdm_class(
         (ex.map)(fn, *iterables, **map_args), **kwargs))


def thread_map(fn, *iterables, **tqdm_kwargs):
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    tqdm_class : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    max_workers : int, optional
        Maximum number of workers to spawn; passed to
        `concurrent.futures.ThreadPoolExecutor.__init__`.
        [default: max(32, cpu_count() + 4)].
    """
    from concurrent.futures import ThreadPoolExecutor
    return _executor_map(ThreadPoolExecutor, fn, *iterables, **tqdm_kwargs)


def process_map(fn, *iterables, **tqdm_kwargs):
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    max_workers : int, optional
        Maximum number of workers to spawn; passed to
        `concurrent.futures.ProcessPoolExecutor.__init__`.
        [default: max(32, cpu_count() + 4)].
    chunksize : int, optional
        Size of chunks sent to worker processes; passed to
        `concurrent.futures.ProcessPoolExecutor.map`. [default: 1].
    """
    from concurrent.futures import ProcessPoolExecutor
    if iterables:
        if 'chunksize' not in tqdm_kwargs:
            longest_iterable_len = max(map(length_hint, iterables))
            if longest_iterable_len > 1000:
                from warnings import warn
                warn(('Iterable length %d > 1000 but `chunksize` is not set. This may seriously degrade multiprocess performance. Set `chunksize=1` or more.' % longest_iterable_len),
                  TqdmWarning,
                  stacklevel=2)
    return _executor_map(ProcessPoolExecutor, fn, *iterables, **tqdm_kwargs)