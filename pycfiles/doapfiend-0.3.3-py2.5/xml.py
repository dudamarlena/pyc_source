# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/xml.py
# Compiled at: 2008-05-25 01:12:37
"""

Serialize DOAP as XML/RDF
=========================

This plugin outputs DOAP in RDF/XML
It basically does nothing because all DOAP today is in RDF/XML.
In the future this may take N3, Turtle, RDFa etc. and convert it to RDF/XML.

"""
__docformat__ = 'epytext'
from elementtree import ElementTree
from doapfiend.plugins.base import Plugin

class OutputPlugin(Plugin):
    """Class for formatting DOAP output"""
    name = 'xml'
    enabled = False
    enable_opt = None

    def __init__(self):
        """Setup RDF/XML OutputPlugin class"""
        super(OutputPlugin, self).__init__()
        self.options = None
        return

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        output.add_option('-x', '--%s' % self.name, action='store_true', dest=self.enable_opt, help='Output DOAP as RDF/XML')
        return (parser, output, search)

    def serialize(self, doap_xml, color=False):
        """
        Serialize RDF/XML DOAP as N3 syntax

        Since the only input we currently have is XML, all this really does
        is parse the XML and raise an exception if it's invalid.
        When we do content negotiation/accept N3 etc., this will serialize.

        @param doap_xml: DOAP in RDF/XML serialization
        @type doap_xml: string

        @rtype: unicode
        @returns: DOAP
        """
        ElementTree.fromstring(doap_xml)
        if hasattr(self.options, 'no_color'):
            color = not self.options.no_color
        if color:
            try:
                from pygments import highlight
                from pygments.lexers import XmlLexer
                from pygments.formatters import TerminalFormatter
            except ImportError:
                return doap_xml
            else:
                return highlight(doap_xml, XmlLexer(), TerminalFormatter(full=False))
        else:
            return doap_xml