# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Analysis/Verifier.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 982 bytes
from binding import *
from ..namespace import llvm
from ..Module import Module
from ..Value import Function
llvm.includes.add('llvm/Analysis/Verifier.h')
VerifierFailureAction = llvm.Enum('VerifierFailureAction', 'AbortProcessAction\n                                     PrintMessageAction\n                                     ReturnStatusAction')
verifyModule = llvm.CustomFunction('verifyModule', 'llvm_verifyModule', PyObjectPtr, ref(Module), VerifierFailureAction, PyObjectPtr)
verifyFunction = llvm.Function('verifyFunction', cast(Bool, bool), ref(Function), VerifierFailureAction)