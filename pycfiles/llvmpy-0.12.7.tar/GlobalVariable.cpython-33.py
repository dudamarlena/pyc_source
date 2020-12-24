# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/GlobalVariable.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1725 bytes
from binding import *
from .namespace import llvm
from .GlobalValue import GlobalValue
GlobalVariable = llvm.Class(GlobalValue)
from .Module import Module
from .Type import Type
from .ADT.StringRef import StringRef
from .Value import Value, User, Constant

@GlobalVariable
class GlobalVariable:
    _downcast_ = (
     Value, User, Constant)
    ThreadLocalMode = Enum('NotThreadLocal, GeneralDynamicTLSModel,\n                              LocalDynamicTLSModel, InitialExecTLSModel,\n                              LocalExecTLSModel\n                           ')
    new = Constructor(ref(Module), ptr(Type), cast(bool, Bool), GlobalValue.LinkageTypes, ptr(Constant), cast(str, StringRef), ptr(GlobalVariable), ThreadLocalMode, cast(int, Unsigned)).require_only(5)
    setThreadLocal = Method(Void, cast(bool, Bool))
    setThreadLocalMode = Method(Void, ThreadLocalMode)
    isThreadLocal = Method(cast(Bool, bool))
    isConstant = Method(cast(Bool, bool))
    setConstant = Method(Void, cast(bool, Bool))
    setInitializer = Method(Void, ptr(Constant))
    getInitializer = Method(ptr(Constant))
    hasInitializer = Method(cast(Bool, bool))
    hasUniqueInitializer = Method(cast(Bool, bool))
    hasDefinitiveInitializer = Method(cast(Bool, bool))