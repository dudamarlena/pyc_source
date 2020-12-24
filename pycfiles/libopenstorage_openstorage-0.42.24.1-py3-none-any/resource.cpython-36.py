# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/resource.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2926 bytes
"""
    pygments.lexers.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for resource definition files.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Comment, String, Number, Operator, Text, Keyword, Name
__all__ = [
 'ResourceLexer']

class ResourceLexer(RegexLexer):
    __doc__ = 'Lexer for `ICU Resource bundles\n    <http://userguide.icu-project.org/locale/resources>`_.\n\n    .. versionadded:: 2.0\n    '
    name = 'ResourceBundle'
    aliases = ['resource', 'resourcebundle']
    filenames = []
    _types = (':table', ':array', ':string', ':bin', ':import', ':intvector', ':int',
              ':alias')
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root':[
      (
       '//.*?$', Comment),
      (
       '"', String, 'string'),
      (
       '-?\\d+', Number.Integer),
      (
       '[,{}]', Operator),
      (
       '([^\\s{:]+)(\\s*)(%s?)' % '|'.join(_types),
       bygroups(Name, Text, Keyword)),
      (
       '\\s+', Text),
      (
       words(_types), Keyword)], 
     'string':[
      (
       '(\\\\x[0-9a-f]{2}|\\\\u[0-9a-f]{4}|\\\\U00[0-9a-f]{6}|\\\\[0-7]{1,3}|\\\\c.|\\\\[abtnvfre\\\'"?\\\\]|\\\\\\{|[^"{\\\\])+',
       String),
      (
       '\\{', String.Escape, 'msgname'),
      (
       '"', String, '#pop')], 
     'msgname':[
      (
       '([^{},]+)(\\s*)', bygroups(Name, String.Escape), ('#pop', 'message'))], 
     'message':[
      (
       '\\{', String.Escape, 'msgname'),
      (
       '\\}', String.Escape, '#pop'),
      (
       '(,)(\\s*)([a-z]+)(\\s*\\})',
       bygroups(Operator, String.Escape, Keyword, String.Escape), '#pop'),
      (
       '(,)(\\s*)([a-z]+)(\\s*)(,)(\\s*)(offset)(\\s*)(:)(\\s*)(-?\\d+)(\\s*)',
       bygroups(Operator, String.Escape, Keyword, String.Escape, Operator, String.Escape, Operator.Word, String.Escape, Operator, String.Escape, Number.Integer, String.Escape), 'choice'),
      (
       '(,)(\\s*)([a-z]+)(\\s*)(,)(\\s*)',
       bygroups(Operator, String.Escape, Keyword, String.Escape, Operator, String.Escape), 'choice'),
      (
       '\\s+', String.Escape)], 
     'choice':[
      (
       '(=|<|>|<=|>=|!=)(-?\\d+)(\\s*\\{)',
       bygroups(Operator, Number.Integer, String.Escape), 'message'),
      (
       '([a-z]+)(\\s*\\{)', bygroups(Keyword.Type, String.Escape), 'str'),
      (
       '\\}', String.Escape, ('#pop', '#pop')),
      (
       '\\s+', String.Escape)], 
     'str':[
      (
       '\\}', String.Escape, '#pop'),
      (
       '\\{', String.Escape, 'msgname'),
      (
       '[^{}]+', String)]}

    def analyse_text(text):
        if text.startswith('root:table'):
            return 1.0