# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\rest_django_jwt\help.py
# Compiled at: 2019-08-31 07:49:58
# Size of source mod 2**32: 492 bytes
"""
-------------------------------------------------
   File Name：     help
   Description :
   Author :       jusk?
   date：          2019/8/31
-------------------------------------------------
   Change Activity:
                   2019/8/31:
-------------------------------------------------
"""

def sum(*values):
    s = 0
    for v in values:
        i = int(v)
        s = s + i

    print(s)


def output():
    print('http://xiaoh.me')