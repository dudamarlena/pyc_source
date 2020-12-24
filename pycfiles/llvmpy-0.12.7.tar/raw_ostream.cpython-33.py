# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/raw_ostream.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 490 bytes
from binding import *
from ..namespace import llvm
from ..LLVMContext import LLVMContext
from ..ADT.StringRef import StringRef

@llvm.Class()
class raw_ostream:
    _include_ = 'llvm/Support/raw_ostream.h'
    delete = Destructor()
    flush = Method()


@llvm.Class(raw_ostream)
class raw_svector_ostream:
    _include_ = 'llvm/Support/raw_os_ostream.h'
    _base_ = raw_ostream
    str = Method(cast(str, StringRef))
    bytes = Method(cast(bytes, StringRef))
    bytes.realname = 'str'