# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/DynamicLibrary.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1417 bytes
from binding import *
from ..namespace import sys
from ..ADT.StringRef import StringRef
DynamicLibrary = sys.Class()

@DynamicLibrary
class DynamicLibrary:
    _include_ = 'llvm/Support/DynamicLibrary.h'
    isValid = Method(cast(Bool, bool))
    getAddressOfSymbol = Method(cast(VoidPtr, int), cast(str, ConstCharPtr))
    LoadPermanentLibrary = CustomStaticMethod('DynamicLibrary_LoadLibraryPermanently', PyObjectPtr, cast(str, ConstCharPtr), PyObjectPtr).require_only(1)
    SearchForAddressOfSymbol = StaticMethod(cast(VoidPtr, int), cast(str, ConstCharPtr))
    AddSymbol = StaticMethod(Void, cast(str, StringRef), cast(int, VoidPtr))
    getPermanentLibrary = CustomStaticMethod('DynamicLibrary_getPermanentLibrary', PyObjectPtr, cast(str, ConstCharPtr), PyObjectPtr).require_only(1)