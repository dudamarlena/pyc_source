# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/hypothesis.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 127 bytes
from hypothesis import strategies as st

def hexstr_strategy():
    return st.from_regex('\\A(0[xX])?[0-9a-fA-F]*\\Z')