# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bplib/bindings.py
# Compiled at: 2019-05-26 14:26:15
import os, platform, cffi
from ._bplib import ffi, lib
_FFI = ffi
_C = lib

def test_load():
    assert _C != None
    assert _FFI != None
    x = _C.BP_GROUP_new()
    return