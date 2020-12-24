# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/libs/task/asynckit.py
# Compiled at: 2016-02-25 04:17:16


class AsyncResultProxy(object):

    def __init__(self, async_result):
        self._async_result = async_result

    def __getattr__(self, name):
        result = self._async_result.get()
        return getattr(self._async_result, name)