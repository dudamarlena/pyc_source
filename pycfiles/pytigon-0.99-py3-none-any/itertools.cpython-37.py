# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/contrib/itertools.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 827 bytes
"""
Thin wrappers around `itertools`.
"""
from __future__ import absolute_import
import tqdm.auto as tqdm_auto
from copy import deepcopy
import itertools
__author__ = {'github.com/': ['casperdcl']}
__all__ = ['product']

def product(*iterables, **tqdm_kwargs):
    """
    Equivalent of `itertools.product`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """
    kwargs = deepcopy(tqdm_kwargs)
    tqdm_class = kwargs.pop('tqdm_class', tqdm_auto)
    try:
        lens = list(map(len, iterables))
    except TypeError:
        total = None
    else:
        total = 1
        for i in lens:
            total *= i

        kwargs.setdefault('total', total)
    with tqdm_class(**kwargs) as (t):
        for i in (itertools.product)(*iterables):
            yield i
            t.update()