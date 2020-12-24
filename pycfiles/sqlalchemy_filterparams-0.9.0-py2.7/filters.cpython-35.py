# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams/filters.py
# Compiled at: 2016-02-20 19:34:56
# Size of source mod 2**32: 2189 bytes
from sqlalchemy import Column, String
from .util import convert, is_type

class Filter:
    name = None

    def __init__(self, converters):
        self.converters = converters

    def __eq__(self, other):
        if isinstance(other, Filter):
            return other.name == self.name
        if isinstance(other, str):
            return self.name == other
        super().__eq__(other)

    def __call__(self, param, value):
        return self.apply(param, value)

    def apply(self, param, value):
        if hasattr(param, 'type'):
            type_cl = param.type
        else:
            type_cl = param
        value = self._convert(type_cl, value)
        return self._apply(param, value)

    def _convert(self, type_cl, value):
        return convert(value, type_cl, self.converters)


class EqFilter(Filter):
    name = 'eq'

    def _apply(self, param, value):
        return param == value


class NeqFilter(Filter):
    name = 'neq'

    def _apply(self, param, value):
        return param != value


class LesserFilter(Filter):
    name = 'lt'

    def _apply(self, param, value):
        return param < value


class LesserEqualFilter(Filter):
    name = 'lte'

    def _apply(self, param, value):
        return param <= value


class GreaterFilter(Filter):
    name = 'gt'

    def _apply(self, param, value):
        return param > value


class GreaterEqualFilter(Filter):
    name = 'gte'

    def _apply(self, param, value):
        return param >= value


class _LikeBase(Filter):

    def apply(self, param, value):
        if not is_type(param.type, String):
            raise ValueError('Like is only possible on string')
        return super().apply(param, value)


class LikeFilter(_LikeBase):
    name = 'like'

    def _apply(self, param, value):
        return param.like(value)


class ILikeFilter(_LikeBase):
    name = 'ilike'

    def _apply(self, param, value):
        return param.ilike(value)


DEFAULT_FILTERS = [
 EqFilter,
 NeqFilter,
 LesserFilter,
 LesserEqualFilter,
 GreaterFilter,
 GreaterEqualFilter,
 LikeFilter,
 ILikeFilter]