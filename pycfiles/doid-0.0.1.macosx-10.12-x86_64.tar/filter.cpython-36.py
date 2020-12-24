# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/paulos/.virtualenvs/doid/lib/python3.6/site-packages/doid/filter.py
# Compiled at: 2018-09-26 01:09:27
# Size of source mod 2**32: 2713 bytes
import abc, operator, re
from functools import reduce

class BaseFilter(object):

    def __call__(self, value):
        raise NotImplementedError

    def _binary(self, other, op):
        this = self

        class Filter(BaseFilter):

            def __call__(self, value):
                return op(this(value), other(value))

        return Filter()

    def _unary(self, op):
        this = self

        class Filter(BaseFilter):

            def __call__(self, value):
                return op(this(value))

        return Filter()

    def __and__(self, other):
        return self._binary(other, operator.and_)

    def __or__(self, other):
        return self._binary(other, operator.or_)

    def __neg__(self):
        return self._unary(operator.neg)

    def __invert__(self):
        this = self

        class Filter(BaseFilter):

            def __call__(self, value):
                return not this(value)

        return Filter()


class FilterDecorator(BaseFilter):

    def __init__(self, fn):
        self._fn = fn

    def __call__(self, value):
        return self._fn(value)


def ga(obj, *args):
    """Get nested attributes"""
    if len(args) > 1:
        return ga(getattr(obj, args[0]), *args[1:])
    else:
        return getattr(obj, args[0])


class Q(FilterDecorator):
    OPS = {'gt':operator.gt, 
     'ge':operator.ge, 
     'lt':operator.lt, 
     'le':operator.le, 
     'ne':operator.ne, 
     'in':operator.contains}

    def __init__(self, *args, **kwargs):
        if args:
            self._fn = reduce(operator.and_, args)
        for clause, value in kwargs.items():
            if not not clause.startswith('__'):
                raise AssertionError('No dunder at the start, please.')
            elif not not clause.endswith('__'):
                raise AssertionError('No dunder at the end, please.')
            super().__init__(self.expression_to_filter(clause, value))

    def expression_to_filter(self, clause, value):
        if '__' not in clause:
            return FilterDecorator(lambda obj: getattr(obj, clause) == value)
        else:
            parts = clause.split('__')
            args = parts[:-1]
            if parts[(-1)] in self.OPS:
                op = self.OPS[parts[(-1)]]
                return FilterDecorator(lambda obj: op(ga(obj, *args), value))
            if parts[(-1)] == 'match':
                return FilterDecorator(lambda obj: bool(re.search(value, ga(obj, *args))))
            if parts[(-1)] == 'imatch':
                return FilterDecorator(lambda obj: bool(re.search(value, ga(obj, *args), re.I)))
            if parts[(-1)] == 'between':
                return FilterDecorator(lambda obj: value[0] <= ga(obj, *args) <= value[1])
            return FilterDecorator(lambda obj: ga(obj, *parts) == value)


doid_filter = FilterDecorator