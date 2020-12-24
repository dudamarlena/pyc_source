# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Pass.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 699 bytes
from binding import *
from .namespace import llvm
Pass = llvm.Class()
ModulePass = llvm.Class(Pass)
FunctionPass = llvm.Class(Pass)
ImmutablePass = llvm.Class(ModulePass)
from .ADT.StringRef import StringRef
from .Module import Module
from .Value import Function

@Pass
class Pass:
    _include_ = 'llvm/Pass.h'
    delete = Destructor()
    getPassName = Method(cast(StdString, str))
    dump = Method()


@ModulePass
class ModulePass:
    runOnModule = Method(cast(Bool, bool), ref(Module))


@FunctionPass
class FunctionPass:
    doInitialization = Method(cast(Bool, bool), ref(Module))
    doFinalization = Method(cast(Bool, bool), ref(Module))


@ImmutablePass
class ImmutablePass:
    pass