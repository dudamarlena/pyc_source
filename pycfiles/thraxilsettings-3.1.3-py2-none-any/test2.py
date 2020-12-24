# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/code/python/thraxilsettings/thraxilsettings/test2.py
# Compiled at: 2015-09-12 13:09:23


def common(**kwargs):
    bar = kwargs['foo'] + ' plus something from test2'
    return locals()