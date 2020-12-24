# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/StringRefMemoryObject.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1086 bytes
from binding import *
from ..namespace import llvm
from ..ADT.StringRef import StringRef
if LLVM_VERSION >= (3, 4):
    MemoryObject = llvm.Class()
    StringRefMemoryObject = llvm.Class(MemoryObject)

    @MemoryObject
    class MemoryObject:
        _include_ = 'llvm/Support/MemoryObject.h'
        getBase = Method(cast(Uint64, int))
        getExtent = Method(cast(Uint64, int))
        readBytes = CustomMethod('MemoryObject_readBytes', PyObjectPtr, cast(int, Uint64), cast(int, Uint64))

        @CustomPythonMethod
        def readAll(self):
            result = self.readBytes(self.getBase(), self.getExtent())
            if not result:
                raise Exception('expected readBytes to be successful!')
            return result


    @StringRefMemoryObject
    class StringRefMemoryObject:
        _include_ = 'llvm/Support/StringRefMemoryObject.h'
        new = Constructor(cast(bytes, StringRef), cast(int, Uint64))