# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/InlineAsm.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 880 bytes
from binding import *
from .namespace import llvm
from .Value import Value
from .DerivedTypes import FunctionType
from .ADT.StringRef import StringRef
if LLVM_VERSION >= (3, 3):
    llvm.includes.add('llvm/IR/InlineAsm.h')
else:
    llvm.includes.add('llvm/InlineAsm.h')
InlineAsm = llvm.Class(Value)

@InlineAsm
class InlineAsm:
    AsmDialect = Enum('AD_ATT', 'AD_Intel')
    ConstraintPrefix = Enum('isInput, isOutput, isClobber')
    get = StaticMethod(ptr(InlineAsm), ptr(FunctionType), cast(str, StringRef), cast(str, StringRef), cast(bool, Bool), cast(bool, Bool), AsmDialect).require_only(4)