# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/droundy/src/latex_snippet/latex_snippet/__init__.py
# Compiled at: 2020-02-26 08:47:58
# Size of source mod 2**32: 244 bytes
from .latex_snippet import lib, ffi

def html_with_solution(s):
    return ffi.string(lib.latex_to_html_with_solution(s.encode())).decode()


def html_omit_solution(s):
    return ffi.string(lib.latex_to_html_omit_solution(s.encode())).decode()