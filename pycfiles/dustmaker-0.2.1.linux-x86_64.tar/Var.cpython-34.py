# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/dustmaker/Var.py
# Compiled at: 2015-10-14 15:55:49
# Size of source mod 2**32: 321 bytes
from enum import IntEnum

class VarType(IntEnum):
    NULL = 0
    BOOL = 1
    UINT = 2
    INT = 3
    FLOAT = 4
    STRING = 5
    VEC2 = 10
    ARRAY = 15


class Var:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Var (%s, %s)' % (repr(self.type), repr(self.value))