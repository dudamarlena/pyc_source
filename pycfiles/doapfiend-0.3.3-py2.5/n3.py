# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/n3.py
# Compiled at: 2008-05-24 23:31:22
"""

Serializer for N3 (Notation 3)
==============================

This is a plugin for formatting DOAP output as N3 (Notation 3) syntax.

"""
__docformat__ = 'epytext'
import logging
from cStringIO import StringIO
from rdflib import ConjunctiveGraph
from doapfiend.plugins.base import Plugin
LOG = logging.getLogger(__name__)

def get_n3(xml_text, color=False):
    """
    Return N3 (Notation 3) text
    Note: Returns string for non-color and unicode for colored text

    @param xml_text: XML/RDF
    @type xml_text: string

    @rtype: unicode or string
    @return: DOAP in Notation 3
    """
    store = ConjunctiveGraph()
    graph = store.parse(StringIO(xml_text), publicID=None, format='xml')
    notation3 = graph.serialize(format='n3')
    if color:
        try:
            from pygments import highlight
            from doapfiend.lexers import Notation3Lexer
            from pygments.formatters import TerminalFormatter
        except ImportError:
            return notation3
        else:
            return highlight(notation3, Notation3Lexer(), TerminalFormatter(full=False))
    else:
        return notation3
    return


class OutputPlugin(Plugin):
    """Class for formatting DOAP output"""
    name = 'n3'
    enabled = False
    enable_opt = None

    def __init__(self):
        """Setup N3 OutputPlugin class"""
        super(OutputPlugin, self).__init__()
        self.options = None
        return

    def serialize(self, doap_xml, color=False):
        """
        Serialize RDF/XML DOAP as N3 syntax

        @param doap_xml: DOAP in RDF/XML serialization
        @type doap_xml: string

        @rtype: unicode
        @return: DOAP in Notation 3
        """
        if hasattr(self, 'options') and hasattr(self.options, 'no_color'):
            color = not self.options.no_color
        return get_n3(doap_xml, color)

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        output.add_option('-n', '--%s' % self.name, action='store_true', dest=self.enable_opt, help='Output DOAP as Notation 3')
        return (parser, output, search)