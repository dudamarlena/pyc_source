# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: examples/transparent.py
# Compiled at: 2011-05-10 05:13:40


def proxy(data):
    return {'remote': '127.0.0.1:8000'}