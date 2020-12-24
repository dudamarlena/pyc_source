# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/bohrium_lexer/__init__.py
# Compiled at: 2016-11-17 03:33:06
__doc__ = '\n    pygments.lexers.bohrium\n    ~~~~~~~~~~~~~~~~~~~~~\n\n    Lexer for Bohrium.\n'
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