# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/deeding.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 336 bytes
"""
deeding.py deed module

Backwards compatibility module
Future use doing module instead

"""
from . import doing
deedify = doing.doify

class Deed(doing.Doer):
    pass


class DeedParam(doing.DoerParam):
    pass


class DeedSince(doing.DoerSince):
    pass


class DeedLapse(doing.DoerLapse):
    pass