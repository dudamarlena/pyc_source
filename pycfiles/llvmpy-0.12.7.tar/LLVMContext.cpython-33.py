# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/LLVMContext.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 263 bytes
from binding import *
from .namespace import llvm

@llvm.Class()
class LLVMContext:
    if LLVM_VERSION >= (3, 3):
        _include_ = 'llvm/IR/LLVMContext.h'
    else:
        _include_ = 'llvm/LLVMContext.h'


llvm.Function('getGlobalContext', ref(LLVMContext))