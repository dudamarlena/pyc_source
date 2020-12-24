# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Transforms/Utils/Cloning.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 727 bytes
from binding import *
from src.namespace import llvm
llvm.includes.add('llvm/Transforms/Utils/Cloning.h')
InlineFunctionInfo = llvm.Class()
from src.Module import Module
from src.Instruction import CallInst

@InlineFunctionInfo
class InlineFunctionInfo:
    new = Constructor()
    delete = Destructor()


CloneModule = llvm.Function('CloneModule', ptr(Module), ptr(Module))
InlineFunction = llvm.Function('InlineFunction', cast(Bool, bool), ptr(CallInst), ref(InlineFunctionInfo), cast(bool, Bool)).require_only(2)