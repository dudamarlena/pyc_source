# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/PassRegistry.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 565 bytes
from binding import *
from .namespace import llvm
from src.ADT.StringRef import StringRef
PassRegistry = llvm.Class()
from src.PassSupport import PassInfo

@PassRegistry
class PassRegistry:
    _include_ = 'llvm/PassRegistry.h'
    delete = Destructor()
    getPassRegistry = StaticMethod(ownedptr(PassRegistry))
    getPassInfo = Method(const(ptr(PassInfo)), cast(str, StringRef))
    enumerate = CustomMethod('PassRegistry_enumerate', PyObjectPtr)