# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/bohrium_lexer/__init__.py
# Compiled at: 2016-11-17 03:33:06
"""
    pygments.lexers.bohrium
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for Bohrium.
"""
import re
from pygments.lexer import RegexLexer
from pygments.token import *

class BohriumLexer(RegexLexer):
    name = 'Bohrium'
    aliases = ['bohrium']
    filenames = ['*.bh']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '\\n|\\s+', Text),
              (
               '#(.*)', Comment.Single),
              (
               '\\.+', Comment.Special),
              (
               '\\d+', Number.Integer),
              (
               '[\\[\\](){};,/?:\\\\]', Punctuation),
              (
               'a\\d+=?\\[', Name.Variable),
              (
               'a\\d+=?\\b', Name.Variable),
              (
               'BH_.*?\\b', Keyword.Operator)]}