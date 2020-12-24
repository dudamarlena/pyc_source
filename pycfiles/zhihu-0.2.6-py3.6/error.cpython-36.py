# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zhihu\error.py
# Compiled at: 2017-07-25 02:12:32
# Size of source mod 2**32: 180 bytes
__author__ = 'liuzhijun'

class ZhihuError(Exception):

    def __init__(self, *args, **kwargs):
        (super(ZhihuError, self).__init__)(*args, **kwargs)