# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sum\sum_file.py
# Compiled at: 2019-02-20 09:44:13
# Size of source mod 2**32: 227 bytes
from package.great_package.fact.fact_file import fact

def sum(n):
    if n == 1:
        return fact(1)
    else:
        return sum(n - 1) + fact(n)


if __name__ == '__main__':
    n = int(input())
    print(sum(n))