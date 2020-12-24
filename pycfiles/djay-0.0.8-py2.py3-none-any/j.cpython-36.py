# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/j.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 4527 bytes
"""
    pygments.lexers.j
    ~~~~~~~~~~~~~~~~~

    Lexer for the J programming language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words, include
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text
__all__ = [
 'JLexer']

class JLexer(RegexLexer):
    __doc__ = '\n    For `J <http://jsoftware.com/>`_ source code.\n\n    .. versionadded:: 2.1\n    '
    name = 'J'
    aliases = ['j']
    filenames = ['*.ijs']
    mimetypes = ['text/x-j']
    validName = '\\b[a-zA-Z]\\w*'
    tokens = {'root':[
      (
       '#!.*$', Comment.Preproc),
      (
       'NB\\..*', Comment.Single),
      (
       '\\n+\\s*Note', Comment.Multiline, 'comment'),
      (
       '\\s*Note.*', Comment.Single),
      (
       '\\s+', Text),
      (
       "'", String, 'singlequote'),
      (
       '0\\s+:\\s*0|noun\\s+define\\s*$', Name.Entity, 'nounDefinition'),
      (
       '(([1-4]|13)\\s+:\\s*0|(adverb|conjunction|dyad|monad|verb)\\s+define)\\b',
       Name.Function, 'explicitDefinition'),
      (
       words(('for_', 'goto_', 'label_'), suffix=(validName + '\\.')), Name.Label),
      (
       words(('assert', 'break', 'case', 'catch', 'catchd', 'catcht', 'continue', 'do', 'else',
       'elseif', 'end', 'fcase', 'for', 'if', 'return', 'select', 'throw', 'try',
       'while', 'whilst'),
         suffix='\\.'), Name.Label),
      (
       validName, Name.Variable),
      (
       words(('ARGV', 'CR', 'CRLF', 'DEL', 'Debug', 'EAV', 'EMPTY', 'FF', 'JVERSION', 'LF',
       'LF2', 'Note', 'TAB', 'alpha17', 'alpha27', 'apply', 'bind', 'boxopen', 'boxxopen',
       'bx', 'clear', 'cutLF', 'cutopen', 'datatype', 'def', 'dfh', 'drop', 'each',
       'echo', 'empty', 'erase', 'every', 'evtloop', 'exit', 'expand', 'fetch', 'file2url',
       'fixdotdot', 'fliprgb', 'getargs', 'getenv', 'hfd', 'inv', 'inverse', 'iospath',
       'isatty', 'isutf8', 'items', 'leaf', 'list', 'nameclass', 'namelist', 'names',
       'nc', 'nl', 'on', 'pick', 'rows', 'script', 'scriptd', 'sign', 'sminfo', 'smoutput',
       'sort', 'split', 'stderr', 'stdin', 'stdout', 'table', 'take', 'timespacex',
       'timex', 'tmoutput', 'toCRLF', 'toHOST', 'toJ', 'tolower', 'toupper', 'type',
       'ucp', 'ucpcount', 'usleep', 'utf8', 'uucp')),
       Name.Function),
      (
       '=[.:]', Operator),
      (
       '[-=+*#$%@!~`^&";:.,<>{}\\[\\]\\\\|/]', Operator),
      (
       '[abCdDeEfHiIjLMoprtT]\\.', Keyword.Reserved),
      (
       '[aDiLpqsStux]\\:', Keyword.Reserved),
      (
       '(_[0-9])\\:', Keyword.Constant),
      (
       '\\(', Punctuation, 'parentheses'),
      include('numbers')], 
     'comment':[
      (
       '[^)]', Comment.Multiline),
      (
       '^\\)', Comment.Multiline, '#pop'),
      (
       '[)]', Comment.Multiline)], 
     'explicitDefinition':[
      (
       '\\b[nmuvxy]\\b', Name.Decorator),
      include('root'),
      (
       '[^)]', Name),
      (
       '^\\)', Name.Label, '#pop'),
      (
       '[)]', Name)], 
     'numbers':[
      (
       '\\b_{1,2}\\b', Number),
      (
       '_?\\d+(\\.\\d+)?(\\s*[ejr]\\s*)_?\\d+(\\.?=\\d+)?', Number),
      (
       '_?\\d+\\.(?=\\d+)', Number.Float),
      (
       '_?\\d+x', Number.Integer.Long),
      (
       '_?\\d+', Number.Integer)], 
     'nounDefinition':[
      (
       '[^)]', String),
      (
       '^\\)', Name.Label, '#pop'),
      (
       '[)]', String)], 
     'parentheses':[
      (
       '\\)', Punctuation, '#pop'),
      include('explicitDefinition'),
      include('root')], 
     'singlequote':[
      (
       "[^']", String),
      (
       "''", String),
      (
       "'", String, '#pop')]}