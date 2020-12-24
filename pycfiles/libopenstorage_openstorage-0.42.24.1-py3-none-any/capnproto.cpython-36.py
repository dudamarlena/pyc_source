# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/capnproto.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2194 bytes
"""
    pygments.lexers.capnproto
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Cap'n Proto schema language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, default
from pygments.token import Text, Comment, Keyword, Name, Literal
__all__ = [
 'CapnProtoLexer']

class CapnProtoLexer(RegexLexer):
    __doc__ = "\n    For `Cap'n Proto <https://capnproto.org>`_ source.\n\n    .. versionadded:: 2.2\n    "
    name = "Cap'n Proto"
    filenames = ['*.capnp']
    aliases = ['capnp']
    flags = re.MULTILINE | re.UNICODE
    tokens = {'root':[
      (
       '#.*?$', Comment.Single),
      (
       '@[0-9a-zA-Z]*', Name.Decorator),
      (
       '=', Literal, 'expression'),
      (
       ':', Name.Class, 'type'),
      (
       '\\$', Name.Attribute, 'annotation'),
      (
       '(struct|enum|interface|union|import|using|const|annotation|extends|in|of|on|as|with|from|fixed)\\b',
       Keyword),
      (
       '[\\w.]+', Name),
      (
       '[^#@=:$\\w]+', Text)], 
     'type':[
      (
       '[^][=;,(){}$]+', Name.Class),
      (
       '[\\[(]', Name.Class, 'parentype'),
      default('#pop')], 
     'parentype':[
      (
       '[^][;()]+', Name.Class),
      (
       '[\\[(]', Name.Class, '#push'),
      (
       '[])]', Name.Class, '#pop'),
      default('#pop')], 
     'expression':[
      (
       '[^][;,(){}$]+', Literal),
      (
       '[\\[(]', Literal, 'parenexp'),
      default('#pop')], 
     'parenexp':[
      (
       '[^][;()]+', Literal),
      (
       '[\\[(]', Literal, '#push'),
      (
       '[])]', Literal, '#pop'),
      default('#pop')], 
     'annotation':[
      (
       '[^][;,(){}=:]+', Name.Attribute),
      (
       '[\\[(]', Name.Attribute, 'annexp'),
      default('#pop')], 
     'annexp':[
      (
       '[^][;()]+', Name.Attribute),
      (
       '[\\[(]', Name.Attribute, '#push'),
      (
       '[])]', Name.Attribute, '#pop'),
      default('#pop')]}