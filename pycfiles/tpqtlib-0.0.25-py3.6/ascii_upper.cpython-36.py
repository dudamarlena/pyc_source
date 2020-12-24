# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/externals/pysideuic/port_v2/ascii_upper.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 1170 bytes
import string
_ascii_trans_table = string.maketrans(string.ascii_lowercase, string.ascii_uppercase)

def ascii_upper(s):
    return s.translate(_ascii_trans_table)