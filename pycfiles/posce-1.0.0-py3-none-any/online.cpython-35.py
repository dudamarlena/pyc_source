# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\procode\login_init\online.py
# Compiled at: 2019-09-03 22:15:01
# Size of source mod 2**32: 810 bytes
__doc__ = '\n与posserviceapi\n'
from posserviceapi.translator import Translator

class OnLineClass(object):
    request = Translator()

    def __init__(self, module):
        self._OnLineClass__module = module

    def get_module(self):
        return self._OnLineClass__module

    @classmethod
    def checkHealth(self, **kwargs):
        self.request.paramtype = 'body'
        self.request.return_v = 'original'
        res = self.request.sendRequest(**kwargs)
        return res

    def checkcpu(self, **kwargs):
        self.request.paramtype = 'query'
        res = self.request.sendRequest(**kwargs)
        return res

    def regiscpu(self, **kwargs):
        self.request.paramtype = 'query'
        res = self.request.sendRequest(**kwargs)
        return res