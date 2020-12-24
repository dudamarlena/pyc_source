# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\great_package\main.py
# Compiled at: 2019-02-20 09:57:57
# Size of source mod 2**32: 78 bytes
from package.great_package.sum import sum
n = int(input())
print(sum(n))