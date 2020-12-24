# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/CodeGen/MachineCodeInfo.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 348 bytes
from binding import *
from ..namespace import llvm
MachineCodeInfo = llvm.Class()

@MachineCodeInfo
class MachineCodeInfo:
    _include_ = 'llvm/CodeGen/MachineCodeInfo.h'
    setSize = Method(Void, cast(int, Size_t))
    setAddress = Method(Void, cast(int, VoidPtr))
    size = Method(cast(Size_t, int))
    address = Method(cast(VoidPtr, int))