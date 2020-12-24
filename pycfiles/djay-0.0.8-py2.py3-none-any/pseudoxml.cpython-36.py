# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/writers/pseudoxml.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 772 bytes
"""
Simple internal document tree Writer, writes indented pseudo-XML.
"""
__docformat__ = 'reStructuredText'
from docutils import writers

class Writer(writers.Writer):
    supported = ('pprint', 'pformat', 'pseudoxml')
    config_section = 'pseudoxml writer'
    config_section_dependencies = ('writers', )
    output = None

    def translate(self):
        self.output = self.document.pformat()

    def supports(self, format):
        """This writer supports all format-specific elements."""
        return True