# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\adrie\Desktop\Programmation\better-exceptions\better_exceptions\highlighter.py
# Compiled at: 2018-03-25 15:51:45
# Size of source mod 2**32: 505 bytes
import pygments, pygments.lexers, pygments.formatters

class Highlighter(object):

    def __init__(self, style='monokai'):
        self._lexer = pygments.lexers.get_lexer_by_name('python3')
        self._formatter = pygments.formatters.get_formatter_by_name('terminal256', style=style)

    def highlight(self, source):
        return pygments.highlight(source, self._lexer, self._formatter)

    def get_tokens(self, source):
        return list(self._lexer.get_tokens_unprocessed(source))