# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Users\Administrator\AppData\Local\Programs\Python\Python36\Lib\site-packages\hytestlib\hylibone.py
# Compiled at: 2019-09-21 07:36:16
# Size of source mod 2**32: 235 bytes


def run():
    print('hy-lib-one: run')


def add(a, b, c):
    print('相加的结果是: %d' % (a + b + c))


if __name__ == '__main__':
    print(__name__)
    add(1, 3, 6)