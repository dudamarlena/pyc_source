# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/common/filterChoices.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 598 bytes
from enum import Enum

class filterChoices(Enum):
    CONTAINS = 'contains'
    NOT_CONTAINS = 'notcontains'
    EQUAL = 'equal'
    NOT_EQUAL = 'notequal'
    GREATER_THAN = 'greater_than'
    GREATER_THAN_EQUAL_TO = 'greater_than_equal_to'
    LESS_THAN = 'less_than'
    LESS_THAN_EQUAL_TO = 'less_than_equal_to'
    BEGIN_WITH = 'begin_with'
    NOT_BEGIN_WITH = 'not_begin_with'
    END_WITH = 'end_with'
    NOT_END_WITH = 'not_end_with'
    EARLIEST = 'earliest'
    LATEST = 'latest'
    BETWEEN = 'between'
    NOT_BETWEEN = 'notbetween'

    def __str__(self):
        return self.value