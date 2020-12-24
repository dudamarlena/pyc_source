# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Bitcode/ReaderWriter.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1521 bytes
from binding import *
from ..namespace import llvm
from ..ADT.StringRef import StringRef
from ..Module import Module
from ..LLVMContext import LLVMContext
llvm.includes.add('llvm/Bitcode/ReaderWriter.h')
ParseBitCodeFile = llvm.CustomFunction('ParseBitCodeFile', 'llvm_ParseBitCodeFile', PyObjectPtr, cast(bytes, StringRef), ref(LLVMContext), PyObjectPtr).require_only(2)
WriteBitcodeToFile = llvm.CustomFunction('WriteBitcodeToFile', 'llvm_WriteBitcodeToFile', PyObjectPtr, ptr(Module), PyObjectPtr)
getBitcodeTargetTriple = llvm.CustomFunction('getBitcodeTargetTriple', 'llvm_getBitcodeTargetTriple', PyObjectPtr, cast(str, StringRef), ref(LLVMContext), PyObjectPtr).require_only(2)