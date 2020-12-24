# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komparse\parser.py
# Compiled at: 2020-03-13 17:42:49
# Size of source mod 2**32: 885 bytes
from .scanner import Scanner
from .translators import Rule
from .char_stream import StringStream

class Parser(object):

    def __init__(self, grammar):
        self._grammar = grammar
        self._root = Rule(self._grammar.get_root_rule())
        self._error = ''

    def get_grammar(self):
        return self._grammar

    def parse(self, source):
        self._error = ''
        scanner = Scanner(StringStream(source), self._grammar)
        nodes = self._root.translate(self._grammar, scanner)
        if not scanner.has_next():
            return nodes and nodes[0] or None
        unexpected_token = scanner.peek()
        self._error = "Unexpected token: '{}' of types '{}'".format(unexpected_token.value, unexpected_token.types)
        return

    def error(self):
        return self._error