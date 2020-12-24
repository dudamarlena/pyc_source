# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/XMLWidgets/WidgetPathScheme.py
# Compiled at: 2008-08-28 08:23:26
from Products.ParsedXML.NodePath.ElementIdPath import ElementIdPathScheme
from WidgetDOM import getWidgetWrappedNode

class WidgetPathScheme(ElementIdPathScheme):
    __module__ = __name__

    def resolve_steps(self, top_node, steps):
        top_node = getWidgetWrappedNode(top_node)
        return ElementIdPathScheme.resolve_steps(self, top_node, steps)