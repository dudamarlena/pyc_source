# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/BasicBlock.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1036 bytes
from binding import *
from .namespace import llvm
from .Value import Function, BasicBlock, Value
from .Instruction import Instruction, TerminatorInst
from .LLVMContext import LLVMContext
from .ADT.StringRef import StringRef

@BasicBlock
class BasicBlock:
    _downcast_ = Value
    Create = StaticMethod(ptr(BasicBlock), ref(LLVMContext), cast(str, StringRef), ptr(Function), ptr(BasicBlock))
    getParent = Method(ptr(Function))
    getTerminator = Method(ptr(TerminatorInst))
    empty = Method(cast(Bool, bool))
    dropAllReferences = Method()
    isLandingPad = Method(cast(Bool, bool))
    removePredecessor = Method(Void, ptr(BasicBlock), cast(bool, Bool))
    removePredecessor |= Method(Void, ptr(BasicBlock))
    getInstList = CustomMethod('BasicBlock_getInstList', PyObjectPtr)
    eraseFromParent = Method()
    splitBasicBlock = Method(ptr(BasicBlock), ptr(Instruction), cast(str, StringRef)).require_only(1)