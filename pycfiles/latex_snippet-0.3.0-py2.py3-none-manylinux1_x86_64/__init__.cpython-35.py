# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/droundy/src/latex_snippet/latex_snippet/__init__.py
# Compiled at: 2019-08-03 18:09:18
# Size of source mod 2**32: 102 bytes
from .latex_snippet import lib, ffi

def html(s):
    return ffi.string(lib.convert_html(s.encode()))