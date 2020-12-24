# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/dynamodb/condition.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3881 bytes
from boto.dynamodb.types import dynamize_value

class Condition(object):
    __doc__ = "\n    Base class for conditions.  Doesn't do a darn thing but allows\n    is to test if something is a Condition instance or not.\n    "

    def __eq__(self, other):
        if isinstance(other, Condition):
            return self.to_dict() == other.to_dict()


class ConditionNoArgs(Condition):
    __doc__ = '\n    Abstract class for Conditions that require no arguments, such\n    as NULL or NOT_NULL.\n    '

    def __repr__(self):
        return '%s' % self.__class__.__name__

    def to_dict(self):
        return {'ComparisonOperator': self.__class__.__name__}


class ConditionOneArg(Condition):
    __doc__ = '\n    Abstract class for Conditions that require a single argument\n    such as EQ or NE.\n    '

    def __init__(self, v1):
        self.v1 = v1

    def __repr__(self):
        return '%s:%s' % (self.__class__.__name__, self.v1)

    def to_dict(self):
        return {'AttributeValueList': [dynamize_value(self.v1)],  'ComparisonOperator': self.__class__.__name__}


class ConditionTwoArgs(Condition):
    __doc__ = '\n    Abstract class for Conditions that require two arguments.\n    The only example of this currently is BETWEEN.\n    '

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.v1, self.v2)

    def to_dict(self):
        values = (
         self.v1, self.v2)
        return {'AttributeValueList': [dynamize_value(v) for v in values],  'ComparisonOperator': self.__class__.__name__}


class ConditionSeveralArgs(Condition):
    __doc__ = '\n    Abstract class for conditions that require several argument (ex: IN).\n    '

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(self.values))

    def to_dict(self):
        return {'AttributeValueList': [dynamize_value(v) for v in self.values], 
         'ComparisonOperator': self.__class__.__name__}


class EQ(ConditionOneArg):
    pass


class NE(ConditionOneArg):
    pass


class LE(ConditionOneArg):
    pass


class LT(ConditionOneArg):
    pass


class GE(ConditionOneArg):
    pass


class GT(ConditionOneArg):
    pass


class NULL(ConditionNoArgs):
    pass


class NOT_NULL(ConditionNoArgs):
    pass


class CONTAINS(ConditionOneArg):
    pass


class NOT_CONTAINS(ConditionOneArg):
    pass


class BEGINS_WITH(ConditionOneArg):
    pass


class IN(ConditionSeveralArgs):
    pass


class BEGINS_WITH(ConditionOneArg):
    pass


class BETWEEN(ConditionTwoArgs):
    pass