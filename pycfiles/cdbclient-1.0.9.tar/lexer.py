# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/lexer.py
# Compiled at: 2016-07-12 21:12:51
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.layout.lexers import SimpleLexer
from prompt_toolkit.token import Token
from .grammar import grammar
lexer = GrammarLexer(grammar, lexers={'command': SimpleLexer(Token.Command), 
   'operand': SimpleLexer(Token.Operand), 
   'database_name': SimpleLexer(Token.Operand)})