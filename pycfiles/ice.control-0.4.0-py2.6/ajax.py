# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/tree/ajax.py
# Compiled at: 2010-08-27 06:32:04
from rfc822 import formatdate, time
from zope.component import getMultiAdapter
from interfaces import IXML

def setHeaders(response):
    response.setHeader('Content-Type', 'text/xml')
    response.setHeader('Pragma', 'no-cache')
    response.setHeader('Cache-Control', 'no-cache')
    response.setHeader('Expires', formatdate(time.time() - 604800))


class Ajax:

    def getControlTreeNode(self):
        setHeaders(self.request.response)
        node = getMultiAdapter((self.context, self.request), IXML)
        return node.node_xmldoc()

    def getControlTreeChildren(self):
        setHeaders(self.request.response)
        node = getMultiAdapter((self.context, self.request), IXML)
        return node.children_xmldoc()