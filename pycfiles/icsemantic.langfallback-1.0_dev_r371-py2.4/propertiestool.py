# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/exportimport/propertiestool.py
# Compiled at: 2008-10-06 10:31:06
"""Plone Properties tool setup handlers.
"""
from Products.CMFPlone.exportimport.propertiestool import SimpleItemWithPropertiesXMLAdapter as BaseAdapter

class SimpleItemWithPropertiesXMLAdapter(BaseAdapter):
    """Node im- and exporter for SimpleItemWithProperties.
    """
    __module__ = __name__

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        obj = self.context
        self._initProperties(node)
        properties = [ child for child in node.childNodes if child.nodeName == 'property' ]
        for property in properties:
            if property.getAttribute('remove') == 'True':
                obj._delProperty(property.getAttribute('name'))