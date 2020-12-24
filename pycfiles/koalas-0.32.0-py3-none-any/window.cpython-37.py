# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/window.py
# Compiled at: 2019-10-04 00:12:44
# Size of source mod 2**32: 2700 bytes
from functools import partial
from typing import Any
from databricks.koalas.missing.window import _MissingPandasLikeRolling, _MissingPandasLikeRollingGroupby, _MissingPandasLikeExpanding, _MissingPandasLikeExpandingGroupby

class _RollingAndExpanding(object):

    def __init__(self, obj):
        self.obj = obj


class Rolling(_RollingAndExpanding):

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeRolling, item):
            property_or_func = getattr(_MissingPandasLikeRolling, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)


class RollingGroupby(Rolling):

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeRollingGroupby, item):
            property_or_func = getattr(_MissingPandasLikeRollingGroupby, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)


class Expanding(_RollingAndExpanding):

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeExpanding, item):
            property_or_func = getattr(_MissingPandasLikeExpanding, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)


class ExpandingGroupby(Expanding):

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeExpandingGroupby, item):
            property_or_func = getattr(_MissingPandasLikeExpandingGroupby, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)