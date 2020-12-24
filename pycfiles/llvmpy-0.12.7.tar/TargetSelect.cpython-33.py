# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/TargetSelect.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1249 bytes
import os
from binding import *
from ..namespace import llvm, default
llvm.includes.add('llvm/Support/TargetSelect.h')
InitializeNativeTarget = llvm.Function('InitializeNativeTarget')
InitializeNativeTargetAsmPrinter = llvm.Function('InitializeNativeTargetAsmPrinter', cast(Bool, bool))
InitializeNativeTargetAsmParser = llvm.Function('InitializeNativeTargetAsmParser', cast(Bool, bool))
InitializeNativeTargetDisassembler = llvm.Function('InitializeNativeTargetDisassembler', cast(Bool, bool))
InitializeAllTargets = llvm.Function('InitializeAllTargets')
InitializeAllTargetInfos = llvm.Function('InitializeAllTargetInfos')
InitializeAllTargetMCs = llvm.Function('InitializeAllTargetMCs')
InitializeAllAsmPrinters = llvm.Function('InitializeAllAsmPrinters')
InitializeAllDisassemblers = llvm.Function('InitializeAllDisassemblers')
InitializeAllAsmParsers = llvm.Function('InitializeAllAsmParsers')
for target in TARGETS_BUILT:
    decls = ('Target', 'TargetInfo', 'TargetMC', 'AsmPrinter')
    for k in map(lambda x: 'LLVMInitialize%s%s' % (target, x), decls):
        if k == 'LLVMInitializeCppBackendAsmPrinter':
            continue
        globals()[k] = default.Function(k)