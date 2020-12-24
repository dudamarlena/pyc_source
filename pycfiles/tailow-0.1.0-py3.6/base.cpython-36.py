# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/operators/base.py
# Compiled at: 2018-06-26 09:23:44
# Size of source mod 2**32: 1831 bytes
from tailow.fields.base import BaseField

class Operator(object):

    def get_value(self, field, value):
        if field is None or not isinstance(field, BaseField):
            return value
        else:
            return field.to_query(value)

    def to_query(self, field_name, value):
        return NotImplementedError()


class OperationRegistry(object):
    _registry = {}

    @classmethod
    def register(cls, name, opr):
        cls._registry[name] = opr

    @classmethod
    def values(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry.get(name)


def transform_query(**queryargs):
    """ transforms the query to mongodb query """
    query_set = {}
    for key, value in queryargs.items():
        values = key.split('__')
        if len(values) > 0:
            operator, field = values[(-1)], values[0]
            opr = OperationRegistry.get(operator)
            query_values = opr.get_value(field, value)
            query_set[key] = query_values
        else:
            query_set[key] = value

    return query_set


class QBase(object):
    __doc__ = ' Base object of all query combination '

    def __init__(self, *qn):
        self.qs = qn

    @property
    def query(self):
        return self.qs

    def __or__(self, other):
        return QCombination(self.query, other.query)

    def __and__(self, other):
        return QConjugation(self.query, other.query)


class QCombination(QBase):

    @property
    def query(self):
        return {'$or': list(self.qs)}


class QConjugation(QBase):

    @property
    def query(self):
        return {'$and': list(self.qs)}


class Q(QBase):

    def __init__(self, **fltr):
        self._transformed = transform_query(**fltr)

    @property
    def query(self):
        return self._transformed