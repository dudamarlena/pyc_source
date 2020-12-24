# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/utils/texttable_utils.py
# Compiled at: 2017-03-01 08:38:06
__author__ = 'UShareSoft'
from texttable import Texttable

def init_texttable(headers, width=200, align=None, types=None):
    table = Texttable(width)
    if headers is not None:
        table.header(headers)
    if align is not None:
        table.set_cols_align(align)
    if types is not None:
        table.set_cols_dtype(types)
    return table