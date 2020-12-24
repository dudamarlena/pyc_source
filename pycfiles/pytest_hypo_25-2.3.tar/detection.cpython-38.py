# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\detection.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 820 bytes
from types import MethodType

def is_hypothesis_test(test):
    if isinstance(test, MethodType):
        return is_hypothesis_test(test.__func__)
    return getattr(test, 'is_hypothesis_test', False)