# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/REST-Server-Skeleton/templates/tpl_client.py
# Compiled at: 2015-04-15 15:26:13
__author__ = 'ruppena'
from twisted.web.template import Element, renderer, XMLFile, XMLString
from twisted.python.filepath import FilePath

class ClientElement(Element):
    loader = XMLFile(FilePath('templates/tpl_client.xml'))

    def __init__(self, _id, _url, _method, _accpettype, _data):
        self.id = _id
        self.url = _url
        self.accept = _accpettype
        self.method = _method
        self.data = _data

    @renderer
    def header(self, request, tag):
        return tag('Header.')

    @renderer
    def clientid(self, request, tag):
        return str(self.id)

    @renderer
    def clienturl(self, request, tag):
        return self.url

    @renderer
    def clientaccept(self, request, tag):
        return self.accept

    @renderer
    def clientmethod(self, request, tag):
        return self.method

    @renderer
    def clientdata(self, request, tag):
        return self.data