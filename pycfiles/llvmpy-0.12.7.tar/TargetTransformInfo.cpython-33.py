# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/TargetTransformInfo.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 805 bytes
from binding import *
from src.namespace import llvm
from src.Pass import ImmutablePass
if LLVM_VERSION >= (3, 3):
    llvm.includes.add('llvm/Analysis/TargetTransformInfo.h')
else:
    llvm.includes.add('llvm/TargetTransformInfo.h')
TargetTransformInfo = llvm.Class(ImmutablePass)
ScalarTargetTransformInfo = llvm.Class()
VectorTargetTransformInfo = llvm.Class()

@ScalarTargetTransformInfo
class ScalarTargetTransformInfo:
    if LLVM_VERSION < (3, 3):
        delete = Destructor()


@VectorTargetTransformInfo
class VectorTargetTransformInfo:
    if LLVM_VERSION < (3, 3):
        delete = Destructor()


@TargetTransformInfo
class TargetTransformInfo:
    if LLVM_VERSION < (3, 3):
        new = Constructor(ptr(ScalarTargetTransformInfo), ptr(VectorTargetTransformInfo))