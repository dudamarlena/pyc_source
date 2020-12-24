# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: //bigfoot/grimmhelga/Production/scripts/libraries/nuke\pysideuic\port_v2\ascii_upper.py
# Compiled at: 2014-04-23 23:47:04
import string
_ascii_trans_table = string.maketrans(string.ascii_lowercase, string.ascii_uppercase)

def ascii_upper(s):
    return s.translate(_ascii_trans_table)