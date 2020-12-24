# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Support/FormattedStream.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 474 bytes
from binding import *
from ..namespace import llvm
from .raw_ostream import raw_ostream

@llvm.Class(raw_ostream)
class formatted_raw_ostream:
    _include_ = 'llvm/Support/FormattedStream.h'
    _new = Constructor(ref(raw_ostream), cast(bool, Bool))

    @CustomPythonStaticMethod
    def new(stream, destroy=False):
        inst = formatted_raw_ostream._new(stream, destroy)
        inst._formatted_raw_ostream__underlying_stream = stream
        return inst