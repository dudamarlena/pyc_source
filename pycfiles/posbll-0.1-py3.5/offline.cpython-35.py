# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\login_init\offline.py
# Compiled at: 2019-09-03 22:17:16
# Size of source mod 2**32: 829 bytes
"""
与poslocaldal交互
"""
from poslocaldal.translator import Translator

class OffLineClass(object):

    def __init__(self, module):
        self._OffLineClass__module = module

    def get_module(self):
        return self._OffLineClass__module

    def checkcpu(self, params=None, apiname=None):
        request = Translator('mytest1.db')
        r = request.getDbObject()
        sql = 'SELECT *  from tester '
        data = r.querylist(sql)
        r.closedb()
        return {'code': 0, 'message': 'eeeerrr', 'data': data}

    def checkcpu1(self, **kwargs):
        request = Translator('mytest1.db')
        r = request.getDbObject()
        sql = 'SELECT *  from tester '
        data = r.querylist(sql)
        r.closedb()
        return {'code': 0, 'message': 'eeeerrr', 'data': data}