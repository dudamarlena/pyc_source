# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Transforms/Utils/BasicBlockUtils.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 767 bytes
from binding import *
from src.namespace import llvm
from src.Value import MDNode
from src.Instruction import Instruction, TerminatorInst
llvm.includes.add('llvm/Transforms/Utils/BasicBlockUtils.h')
SplitBlockAndInsertIfThen = llvm.Function('SplitBlockAndInsertIfThen', ptr(TerminatorInst), ptr(Instruction), cast(bool, Bool), ptr(MDNode))
ReplaceInstWithInst = llvm.Function('ReplaceInstWithInst', Void, ptr(Instruction), ptr(Instruction))