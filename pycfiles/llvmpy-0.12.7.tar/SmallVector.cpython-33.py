# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/ADT/SmallVector.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 387 bytes
from binding import *
from ..namespace import llvm

@llvm.Class()
class SmallVector_Type:
    _realname_ = 'SmallVector<llvm::Type*,8>'
    delete = Destructor()


@llvm.Class()
class SmallVector_Value:
    _realname_ = 'SmallVector<llvm::Value*,8>'
    delete = Destructor()


@llvm.Class()
class SmallVector_Unsigned:
    _realname_ = 'SmallVector<unsigned,8>'
    delete = Destructor()