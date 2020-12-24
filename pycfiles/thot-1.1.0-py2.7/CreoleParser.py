# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/plugins/CreoleParser.py
# Compiled at: 2013-03-05 21:43:25
from creole import creole2html
from thot.parser import Parser
__all__ = [
 'CreoleParser']

class CreoleParser(Parser):
    """Creole to HTML parser."""
    output_ext = 'html'
    parses = ['creole', 'cre']

    def _parse_text(self):
        self.text = creole2html(self.text)