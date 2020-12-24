# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mapnamindsdk/WS.py
# Compiled at: 2020-01-09 03:21:30
# Size of source mod 2**32: 1070 bytes
import cherrypy

@cherrypy.popargs('key')
class MindSdkWebService:
    _MindSdkWebService__instance = None

    @staticmethod
    def getInstance():
        if MindSdkWebService._MindSdkWebService__instance == None:
            MindSdkWebService()
        return MindSdkWebService._MindSdkWebService__instance

    results = {}
    list_dict = {}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(key):
        return MindSdkWebService.results[key]

    @cherrypy.expose
    def getResult(key):
        return MindSdkWebService.results[key]

    @cherrypy.expose
    def getList(key):
        return MindSdkWebService.list_dict[key]

    def set(key, value):
        MindSdkWebService.results[key] = value
        return 'aaa'

    def add(key, value):
        if MindSdkWebService.list_dict.get(key) == None:
            MindSdkWebService.list_dict[key] = []
        MindSdkWebService.list_dict[key].append(value)


if __name__ == '__main__':
    print('started')