# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/rnc.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1990 bytes
"""
    pygments.lexers.rnc
    ~~~~~~~~~~~~~~~~~~~

    Lexer for Relax-NG Compact syntax

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation
__all__ = [
 'RNCCompactLexer']

class RNCCompactLexer(RegexLexer):
    __doc__ = '\n    For `RelaxNG-compact <http://relaxng.org>`_ syntax.\n\n    .. versionadded:: 2.2\n    '
    name = 'Relax-NG Compact'
    aliases = ['rnc', 'rng-compact']
    filenames = ['*.rnc']
    tokens = {'root':[
      (
       'namespace\\b', Keyword.Namespace),
      (
       '(?:default|datatypes)\\b', Keyword.Declaration),
      (
       '##.*$', Comment.Preproc),
      (
       '#.*$', Comment.Single),
      (
       '"[^"]*"', String.Double),
      (
       '(?:element|attribute|mixed)\\b', Keyword.Declaration, 'variable'),
      (
       '(text\\b|xsd:[^ ]+)', Keyword.Type, 'maybe_xsdattributes'),
      (
       '[,?&*=|~]|>>', Operator),
      (
       '[(){}]', Punctuation),
      (
       '.', Text)], 
     'variable':[
      (
       '[^{]+', Name.Variable),
      (
       '\\{', Punctuation, '#pop')], 
     'maybe_xsdattributes':[
      (
       '\\{', Punctuation, 'xsdattributes'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '.', Text)], 
     'xsdattributes':[
      (
       '[^ =}]', Name.Attribute),
      (
       '=', Operator),
      (
       '"[^"]*"', String.Double),
      (
       '\\}', Punctuation, '#pop'),
      (
       '.', Text)]}