# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/dalvik.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 4420 bytes
"""
    pygments.lexers.dalvik
    ~~~~~~~~~~~~~~~~~~~~~~

    Pygments lexers for Dalvik VM-related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Keyword, Text, Comment, Name, String, Number, Punctuation
__all__ = [
 'SmaliLexer']

class SmaliLexer(RegexLexer):
    __doc__ = '\n    For `Smali <http://code.google.com/p/smali/>`_ (Android/Dalvik) assembly\n    code.\n\n    .. versionadded:: 1.6\n    '
    name = 'Smali'
    aliases = ['smali']
    filenames = ['*.smali']
    mimetypes = ['text/smali']
    tokens = {'root':[
      include('comment'),
      include('label'),
      include('field'),
      include('method'),
      include('class'),
      include('directive'),
      include('access-modifier'),
      include('instruction'),
      include('literal'),
      include('punctuation'),
      include('type'),
      include('whitespace')], 
     'directive':[
      (
       '^[ \\t]*\\.(class|super|implements|field|subannotation|annotation|enum|method|registers|locals|array-data|packed-switch|sparse-switch|catchall|catch|line|parameter|local|prologue|epilogue|source)',
       Keyword),
      (
       '^[ \\t]*\\.end (field|subannotation|annotation|method|array-data|packed-switch|sparse-switch|parameter|local)',
       Keyword),
      (
       '^[ \\t]*\\.restart local', Keyword)], 
     'access-modifier':[
      (
       '(public|private|protected|static|final|synchronized|bridge|varargs|native|abstract|strictfp|synthetic|constructor|declared-synchronized|interface|enum|annotation|volatile|transient)',
       Keyword)], 
     'whitespace':[
      (
       '\\n', Text),
      (
       '\\s+', Text)], 
     'instruction':[
      (
       '\\b[vp]\\d+\\b', Name.Builtin),
      (
       '\\b[a-z][A-Za-z0-9/-]+\\s+', Text)], 
     'literal':[
      (
       '".*"', String),
      (
       '0x[0-9A-Fa-f]+t?', Number.Hex),
      (
       '[0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '[0-9]+L?', Number.Integer)], 
     'field':[
      (
       '(\\$?\\b)([\\w$]*)(:)',
       bygroups(Punctuation, Name.Variable, Punctuation))], 
     'method':[
      (
       '<(?:cl)?init>', Name.Function),
      (
       '(\\$?\\b)([\\w$]*)(\\()',
       bygroups(Punctuation, Name.Function, Punctuation))], 
     'label':[
      (
       ':\\w+', Name.Label)], 
     'class':[
      (
       '(L)((?:[\\w$]+/)*)([\\w$]+)(;)',
       bygroups(Keyword.Type, Text, Name.Class, Text))], 
     'punctuation':[
      (
       '->', Punctuation),
      (
       '[{},():=.-]', Punctuation)], 
     'type':[
      (
       '[ZBSCIJFDV\\[]+', Keyword.Type)], 
     'comment':[
      (
       '#.*?\\n', Comment)]}

    def analyse_text(text):
        score = 0
        if re.search('^\\s*\\.class\\s', text, re.MULTILINE):
            score += 0.5
            if re.search('\\b((check-cast|instance-of|throw-verification-error)\\b|(-to|add|[ais]get|[ais]put|and|cmpl|const|div|if|invoke|move|mul|neg|not|or|rem|return|rsub|shl|shr|sub|ushr)[-/])|{|}', text, re.MULTILINE):
                score += 0.3
        if re.search('(\\.(catchall|epilogue|restart local|prologue)|\\b(array-data|class-change-error|declared-synchronized|(field|inline|vtable)@0x[0-9a-fA-F]|generic-error|illegal-class-access|illegal-field-access|illegal-method-access|instantiation-error|no-error|no-such-class|no-such-field|no-such-method|packed-switch|sparse-switch))\\b', text, re.MULTILINE):
            score += 0.6
        return score