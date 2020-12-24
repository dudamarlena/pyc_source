# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sum/sum_file.py
# Compiled at: 2019-02-20 05:59:13
# Size of source mod 2**32: 142 bytes
from test_package_cookiebus.fact.fact_file import fact

def sum(n):
    if n == 1:
        return fact(1)
    return sum(n - 1) + fact(n)