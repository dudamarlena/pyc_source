# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Target/TargetOptions.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 221 bytes
from binding import *
from src.namespace import llvm
llvm.includes.add('llvm/Target/TargetOptions.h')
TargetOptions = llvm.Class()

@TargetOptions
class TargetOptions:
    new = Constructor()
    delete = Destructor()