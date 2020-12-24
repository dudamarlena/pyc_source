# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/PassSupport.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 862 bytes
from binding import *
from .namespace import llvm
PassInfo = llvm.Class()
from src.Pass import Pass
from src.PassRegistry import PassRegistry

@PassInfo
class PassInfo:
    _include_ = 'llvm/PassSupport.h'
    createPass = Method(ptr(Pass))


llvm.Function('initializeCore', Void, ref(PassRegistry))
llvm.Function('initializeScalarOpts', Void, ref(PassRegistry))
llvm.Function('initializeVectorization', Void, ref(PassRegistry))
llvm.Function('initializeIPO', Void, ref(PassRegistry))
llvm.Function('initializeAnalysis', Void, ref(PassRegistry))
llvm.Function('initializeIPA', Void, ref(PassRegistry))
llvm.Function('initializeTransformUtils', Void, ref(PassRegistry))
llvm.Function('initializeInstCombine', Void, ref(PassRegistry))
llvm.Function('initializeInstrumentation', Void, ref(PassRegistry))
llvm.Function('initializeTarget', Void, ref(PassRegistry))