# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\great_package\fact\fact_file.py
# Compiled at: 2019-02-20 05:15:11
# Size of source mod 2**32: 159 bytes


def fact(n):
    if n == 1:
        return 1
    else:
        return fact(n - 1) * n


if __name__ == '__main__':
    n = int(input())
    print(fact(n))