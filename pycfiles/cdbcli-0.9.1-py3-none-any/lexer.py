# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/lexer.py
# Compiled at: 2016-07-12 21:12:51
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.layout.lexers import SimpleLexer
from prompt_toolkit.token import Token
from .grammar import grammar
lexer = GrammarLexer(grammar, lexers={'command': SimpleLexer(Token.Command), 
   'operand': SimpleLexer(Token.Operand), 
   'database_name': SimpleLexer(Token.Operand)})