# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellexer/topic_modelling/main.py
# Compiled at: 2019-04-16 06:25:42
# Size of source mod 2**32: 666 bytes
from ..core.request_handler import BaseRequest

class TopicModelling(BaseRequest):
    __slots__ = BaseRequest.__slots__
    json = True

    @staticmethod
    def builder(response):
        return response

    def url(self, url):
        path = 'getTopicsFromUrl'
        fields = {'url': url}
        response = self._get(path=path, fields=fields)
        return response

    def text(self, text):
        path = 'getTopicsFromText'
        fields = {}
        response = self._post(path=path, fields=fields, body=text)
        return response

    def file(self, file):
        path = 'getTopicsFromFile'
        fields = {'filename': file.name}
        response = self._post(path=path, fields=fields, body=file)
        return response