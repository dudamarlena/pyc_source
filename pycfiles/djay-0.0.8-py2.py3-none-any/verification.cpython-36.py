# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/verification.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3705 bytes
"""
    pygments.lexers.verification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Intermediate Verification Languages (IVLs).

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, words
from pygments.token import Comment, Operator, Keyword, Name, Number, Punctuation, Whitespace
__all__ = [
 'BoogieLexer', 'SilverLexer']

class BoogieLexer(RegexLexer):
    __doc__ = '\n    For `Boogie <https://boogie.codeplex.com/>`_ source code.\n\n    .. versionadded:: 2.1\n    '
    name = 'Boogie'
    aliases = ['boogie']
    filenames = ['*.bpl']
    tokens = {'root':[
      (
       '\\n', Whitespace),
      (
       '\\s+', Whitespace),
      (
       '//[/!](.*?)\\n', Comment.Doc),
      (
       '//(.*?)\\n', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       words(('axiom', 'break', 'call', 'ensures', 'else', 'exists', 'function', 'forall',
       'if', 'invariant', 'modifies', 'procedure', 'requires', 'then', 'var', 'while'),
         suffix='\\b'), Keyword),
      (
       words(('const', ), suffix='\\b'), Keyword.Reserved),
      (
       words(('bool', 'int', 'ref'), suffix='\\b'), Keyword.Type),
      include('numbers'),
      (
       '(>=|<=|:=|!=|==>|&&|\\|\\||[+/\\-=>*<\\[\\]])', Operator),
      (
       '([{}():;,.])', Punctuation),
      (
       '[a-zA-Z_]\\w*', Name)], 
     'comment':[
      (
       '[^*/]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'numbers':[
      (
       '[0-9]+', Number.Integer)]}


class SilverLexer(RegexLexer):
    __doc__ = '\n    For `Silver <https://bitbucket.org/viperproject/silver>`_ source code.\n\n    .. versionadded:: 2.2\n    '
    name = 'Silver'
    aliases = ['silver']
    filenames = ['*.sil', '*.vpr']
    tokens = {'root':[
      (
       '\\n', Whitespace),
      (
       '\\s+', Whitespace),
      (
       '//[/!](.*?)\\n', Comment.Doc),
      (
       '//(.*?)\\n', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       words(('result', 'true', 'false', 'null', 'method', 'function', 'predicate', 'program',
       'domain', 'axiom', 'var', 'returns', 'field', 'define', 'requires', 'ensures',
       'invariant', 'fold', 'unfold', 'inhale', 'exhale', 'new', 'assert', 'assume',
       'goto', 'while', 'if', 'elseif', 'else', 'fresh', 'constraining', 'Seq', 'Set',
       'Multiset', 'union', 'intersection', 'setminus', 'subset', 'unfolding', 'in',
       'old', 'forall', 'exists', 'acc', 'wildcard', 'write', 'none', 'epsilon',
       'perm', 'unique', 'apply', 'package', 'folding', 'label', 'forperm'),
         suffix='\\b'), Keyword),
      (
       words(('Int', 'Perm', 'Bool', 'Ref'), suffix='\\b'), Keyword.Type),
      include('numbers'),
      (
       '[!%&*+=|?:<>/\\-\\[\\]]', Operator),
      (
       '([{}():;,.])', Punctuation),
      (
       '[\\w$]\\w*', Name)], 
     'comment':[
      (
       '[^*/]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'numbers':[
      (
       '[0-9]+', Number.Integer)]}