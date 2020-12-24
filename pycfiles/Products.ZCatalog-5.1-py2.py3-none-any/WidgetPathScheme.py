# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/XMLWidgets/WidgetPathScheme.py
# Compiled at: 2008-08-28 08:23:26
from Products.ParsedXML.NodePath.ElementIdPath import ElementIdPathScheme
from WidgetDOM import getWidgetWrappedNode

class WidgetPathScheme(ElementIdPathScheme):
    __module__ = __name__

    def resolve_steps(self, top_node, steps):
        top_node = getWidgetWrappedNode(top_node)
        return ElementIdPathScheme.resolve_steps(self, top_node, steps)