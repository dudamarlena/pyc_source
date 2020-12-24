# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/highlight.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..elements.elementbase import Attribute, LogicElement
from .. import syntax

class Highlight(LogicElement):
    """This tag is used by the Moya debug library to syntax highlight code (turning it into HTML in the process)."""

    class Help:
        synopsis = b'syntax highlight code'

    dst = Attribute(b'Destination to store exception object', type=b'reference', required=True)
    code = Attribute(b'Code to highlight', type=b'reference', required=True)
    format = Attribute(b'Format of code', required=True, default=b'xml')
    highlight = Attribute(b'Line numbers to highlight', type=b'expression', required=False, default=None)

    def logic(self, context):
        params = self.get_parameters(context)
        highlight = params.highlight or []
        if not isinstance(highlight, list):
            highlight = [
             highlight]
        code = context[params.code]
        html = syntax.highlight(params.format, code, highlight_lines=highlight)
        context[params.dst] = html