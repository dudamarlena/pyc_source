# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/PassManager.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 737 bytes
from binding import *
from .namespace import llvm
PassManagerBase = llvm.Class()
PassManager = llvm.Class(PassManagerBase)
FunctionPassManager = llvm.Class(PassManagerBase)
from .Pass import Pass
from .Module import Module
from .Value import Function

@PassManagerBase
class PassManagerBase:
    _include_ = 'llvm/PassManager.h'
    delete = Destructor()
    add = Method(Void, ownedptr(Pass))


@PassManager
class PassManager:
    new = Constructor()
    run = Method(cast(Bool, bool), ref(Module))


@FunctionPassManager
class FunctionPassManager:
    new = Constructor(ptr(Module))
    run = Method(cast(Bool, bool), ref(Function))
    doInitialization = Method(cast(Bool, bool))
    doFinalization = Method(cast(Bool, bool))