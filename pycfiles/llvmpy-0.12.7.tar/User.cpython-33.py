# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/User.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 293 bytes
from binding import *
from .namespace import llvm
from .Value import Value, User

@User
class User:
    _downcast_ = Value
    getOperand = Method(ptr(Value), cast(int, Unsigned))
    setOperand = Method(Void, cast(int, Unsigned), ptr(Value))
    getNumOperands = Method(cast(Unsigned, int))