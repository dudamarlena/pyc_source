# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/xmlutils.py
# Compiled at: 2019-02-14 00:35:17
"""
Utilities for XML generation/parsing.
"""
import re
from xml.sax.saxutils import XMLGenerator

class UnserializableContentError(ValueError):
    pass


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

    def characters(self, content):
        if content and re.search('[\\x00-\\x08\\x0B-\\x0C\\x0E-\\x1F]', content):
            raise UnserializableContentError('Control characters are not supported in XML 1.0')
        XMLGenerator.characters(self, content)