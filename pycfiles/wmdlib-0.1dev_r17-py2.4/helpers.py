# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wmdlib\tests\helpers.py
# Compiled at: 2007-09-09 17:11:25
from comtypes import COMError
from wmdlib.lowlevel.errorcodes import *

def com_optional_func(fun):
    """Decorator for test function that test an optional COM function.
    (That might return E_NOTIMPL)"""

    def newfun(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except COMError, ce:
            if not ce.hresult + 4294967296 == E_NOTIMPL:
                raise ce

    newfun.__name__ = fun.__name__
    return newfun