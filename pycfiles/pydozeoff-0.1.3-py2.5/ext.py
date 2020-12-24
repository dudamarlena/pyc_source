# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pydozeoff/template/ext.py
# Compiled at: 2010-03-18 23:00:33
"""
Provides useful template engine extensions.
"""
from jinja2 import nodes
from jinja2.ext import Extension
from pydozeoff.template import highlight
from pydozeoff.conf import settings

class CodeHighlightExtension(Extension):
    """Extension that highlights source code.
    """
    tags = set(['code'])

    def __init__(self, environment):
        super(CodeHighlightExtension, self).__init__(environment)

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        args = []
        if not parser.stream.current.test('block_end'):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))
        body = parser.parse_statements(['name:endcode'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_highlight_support', args), [], [], body).set_lineno(lineno)

    def _highlight_support(self, language, caller):
        code = caller()
        return highlight.code(language, code)


class CodeHighlightStyleExtension(Extension):
    """Extension that renders the CSS used to style highlighted source code.
    """
    tags = set(['code_highlight_css'])

    def __init__(self, environment):
        super(CodeHighlightStyleExtension, self).__init__(environment)

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        return nodes.CallBlock(self.call_method('_highlight_style_support', []), [], [], []).set_lineno(lineno)

    def _highlight_style_support(self, caller):
        return '<style type="text/css">%s</style>' % highlight.get_style_defs(settings['SYNTAX_HIGHLIGHT_OPTIONS']['style'])


code = CodeHighlightExtension
code_style = CodeHighlightStyleExtension