# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/logic_types.py
# Compiled at: 2019-01-29 09:32:34
# Size of source mod 2**32: 641 bytes
from enum import Enum

class ExpectationType(Enum):
    __doc__ = '\n    Tells if an boolean expression is expected to be\n    True (POSITIVE) or False (NEGATIVE)\n    '
    POSITIVE = 0
    NEGATIVE = 1


def from_is_negated(is_negated: bool) -> ExpectationType:
    if is_negated:
        return ExpectationType.NEGATIVE
    return ExpectationType.POSITIVE


def negation(expectation_type: ExpectationType) -> ExpectationType:
    if expectation_type is ExpectationType.NEGATIVE:
        return ExpectationType.POSITIVE
    return ExpectationType.NEGATIVE


class Quantifier(Enum):
    __doc__ = 'A logic quantifier'
    ALL = 1
    EXISTS = 2