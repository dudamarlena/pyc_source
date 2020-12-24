# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/windtalker-project/windtalker/py23.py
# Compiled at: 2020-03-04 17:13:17
# Size of source mod 2**32: 388 bytes
"""
A portable version of ``six``, provide basic python2/3 compatible utilities.
"""
import sys
if sys.version_info[0] == 3:
    str_type = str
    int_type = (int,)
    pk_protocol = 3
    is_py2 = False
    is_py3 = True
else:
    str_type = basestring
    int_type = (int, long)
    pk_protocol = 2
    is_py2 = True
    is_py3 = False