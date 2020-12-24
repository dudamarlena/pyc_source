# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\waves\getarray.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 202 bytes


def getarray(d):
    p = ['_' not in k for k in d.keys()]
    for i in range(len(p)):
        if p[i]:
            return d[d.keys()[i]]