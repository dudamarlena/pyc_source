# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/contrib/concurrent.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 1989 bytes
"""
Thin wrappers around `concurrent.futures`.
"""
from __future__ import absolute_import
import tqdm.auto as tqdm_auto
from copy import deepcopy
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
    """
    kwargs = deepcopy(tqdm_kwargs)
    if 'total' not in kwargs:
        kwargs['total'] = len(iterables[0])
    tqdm_class = kwargs.pop('tqdm_class', tqdm_auto)
    max_workers = kwargs.pop('max_workers', min(32, cpu_count() + 4))
    pool_kwargs = dict(max_workers=max_workers)
    if sys.version_info[:2] >= (3, 7):
        pool_kwargs.update(initializer=(tqdm_class.set_lock),
          initargs=(tqdm_class.get_lock(),))
    with PoolExecutor(**pool_kwargs) as (ex):
        return list(tqdm_class((ex.map)(fn, *iterables), **kwargs))


def thread_map(fn, *iterables, **tqdm_kwargs):
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """
    from concurrent.futures import ThreadPoolExecutor
    return _executor_map(ThreadPoolExecutor, fn, *iterables, **tqdm_kwargs)


def process_map(fn, *iterables, **tqdm_kwargs):
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ProcessPoolExecutor`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """
    from concurrent.futures import ProcessPoolExecutor
    return _executor_map(ProcessPoolExecutor, fn, *iterables, **tqdm_kwargs)