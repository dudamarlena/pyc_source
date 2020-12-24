# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/plugins/MarkdownParser.py
# Compiled at: 2013-03-05 21:43:25
import markdown
from thot.parser import Parser
__all__ = [
 'MarkdownParser']

class MarkdownParser(Parser):
    """Markdown Parser"""
    output_ext = 'html'
    parses = ['md', 'markdown']

    def _parse_text(self):
        self.text = markdown.markdown(self.text, [
         'codehilite(css_class=highlight)'])