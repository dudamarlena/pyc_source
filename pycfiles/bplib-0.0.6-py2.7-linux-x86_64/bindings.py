# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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