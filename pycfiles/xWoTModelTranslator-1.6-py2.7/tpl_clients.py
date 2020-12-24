# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/REST-Server-Skeleton/templates/tpl_clients.py
# Compiled at: 2014-12-10 09:56:30
from twisted.web.template import Element, TagLoader, renderer, XMLFile, XMLString
from twisted.python.filepath import FilePath

class ClientsElement(Element):
    loader = XMLFile(FilePath('templates/tpl_clients.xml'))
    widgetData = [(2, 'http://example2.com/notif', 'POST', 'application/xml', 1), (1, 'http://example.com/notif', 'POST', 'application/xml', 1), (3, 'http://example3.com/notif', 'POST', 'application/xml', 1)]

    def __init__(self, clients):
        self.clients = clients

    @renderer
    def header(self, request, tag):
        return tag('Header.')

    @renderer
    def myclients(self, request, tag):
        for widget in self.clients:
            clonedtag = tag.clone()
            clonedtag.fillSlots(id=str(widget[0]))
            clonedtag.fillSlots(uri=str(widget[1]))
            clonedtag.fillSlots(method=str(widget[2]))
            clonedtag.fillSlots(accept=str(widget[3]))
            yield clonedtag

    @renderer
    def widgets(self, request, tag):
        for widget in self.widgetData:
            yield tag.clone().fillSlots(widgetName=widget[1])