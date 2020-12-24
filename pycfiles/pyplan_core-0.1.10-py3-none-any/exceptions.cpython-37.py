# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/cubepy/exceptions.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 735 bytes


class AxisAlignError(ValueError):
    __doc__ = '\n    This error is raised when axis A is being aligned to axis B and:\n    - A is Series:\n      if any value on axis A does not equal to the corresponding value on axis B (order is significant)\n      note that it does not matter if B is Index or Series\n    - A is Index and B is Series:\n      if B contains a value which is not contained in A\n    - A and B are both Index objects and one of them contains a value which is not in the other one \n      (this is also the case when they have different lengths); \n      note that the order of the values can be arbitrary      \n    '


class InvalidAxisLengthError(ValueError):
    pass


class NonUniqueDimNamesError(ValueError):
    pass