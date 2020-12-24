# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\procode\login_init\offline.py
# Compiled at: 2019-09-03 22:17:16
# Size of source mod 2**32: 829 bytes
__doc__ = '\n与poslocaldal交互\n'
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