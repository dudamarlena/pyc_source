# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/xmlutils.py
# Compiled at: 2018-07-11 18:15:30
"""
Utilities for XML generation/parsing.
"""
from xml.sax.saxutils import XMLGenerator

class SimplerXMLGenerator(XMLGenerator):

    def addQuickElement(self, name, contents=None, attrs=None):
        """Convenience method for adding an element with no children"""
        if attrs is None:
            attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents)
        self.endElement(name)
        return