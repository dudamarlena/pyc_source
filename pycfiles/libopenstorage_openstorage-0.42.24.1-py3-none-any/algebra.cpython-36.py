# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/algebra.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 7201 bytes
"""
    pygments.lexers.algebra
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for computer algebra systems.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'GAPLexer', 'MathematicaLexer', 'MuPADLexer', 'BCLexer']

class GAPLexer(RegexLexer):
    __doc__ = '\n    For `GAP <http://www.gap-system.org>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'GAP'
    aliases = ['gap']
    filenames = ['*.g', '*.gd', '*.gi', '*.gap']
    tokens = {'root': [
              (
               '#.*$', Comment.Single),
              (
               '"(?:[^"\\\\]|\\\\.)*"', String),
              (
               '\\(|\\)|\\[|\\]|\\{|\\}', Punctuation),
              (
               '(?x)\\b(?:\n                if|then|elif|else|fi|\n                for|while|do|od|\n                repeat|until|\n                break|continue|\n                function|local|return|end|\n                rec|\n                quit|QUIT|\n                IsBound|Unbind|\n                TryNextMethod|\n                Info|Assert\n              )\\b', Keyword),
              (
               '(?x)\\b(?:\n                true|false|fail|infinity\n              )\\b',
               Name.Constant),
              (
               '(?x)\\b(?:\n                (Declare|Install)([A-Z][A-Za-z]+)|\n                   BindGlobal|BIND_GLOBAL\n              )\\b',
               Name.Builtin),
              (
               '\\.|,|:=|;|=|\\+|-|\\*|/|\\^|>|<', Operator),
              (
               '(?x)\\b(?:\n                and|or|not|mod|in\n              )\\b',
               Operator.Word),
              (
               '(?x)\n              (?:\\w+|`[^`]*`)\n              (?:::\\w+|`[^`]*`)*', Name.Variable),
              (
               '[0-9]+(?:\\.[0-9]*)?(?:e[0-9]+)?', Number),
              (
               '\\.[0-9]+(?:e[0-9]+)?', Number),
              (
               '.', Text)]}


class MathematicaLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Mathematica <http://www.wolfram.com/mathematica/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Mathematica'
    aliases = ['mathematica', 'mma', 'nb']
    filenames = ['*.nb', '*.cdf', '*.nbp', '*.ma']
    mimetypes = ['application/mathematica',
     'application/vnd.wolfram.mathematica',
     'application/vnd.wolfram.mathematica.package',
     'application/vnd.wolfram.cdf']
    operators = (';;', '=', '=.', '!===', ':=', '->', ':>', '/.', '+', '-', '*', '/',
                 '^', '&&', '||', '!', '<>', '|', '/;', '?', '@', '//', '/@', '@@',
                 '@@@', '~~', '===', '&', '<', '>', '<=', '>=')
    punctuation = (',', ';', '(', ')', '[', ']', '{', '}')

    def _multi_escape(entries):
        return '(%s)' % '|'.join(re.escape(entry) for entry in entries)

    tokens = {'root': [
              (
               '(?s)\\(\\*.*?\\*\\)', Comment),
              (
               '([a-zA-Z]+[A-Za-z0-9]*`)', Name.Namespace),
              (
               '([A-Za-z0-9]*_+[A-Za-z0-9]*)', Name.Variable),
              (
               '#\\d*', Name.Variable),
              (
               '([a-zA-Z]+[a-zA-Z0-9]*)', Name),
              (
               '-?\\d+\\.\\d*', Number.Float),
              (
               '-?\\d*\\.\\d+', Number.Float),
              (
               '-?\\d+', Number.Integer),
              (
               words(operators), Operator),
              (
               words(punctuation), Punctuation),
              (
               '".*?"', String),
              (
               '\\s+', Text.Whitespace)]}


class MuPADLexer(RegexLexer):
    __doc__ = '\n    A `MuPAD <http://www.mupad.com>`_ lexer.\n    Contributed by Christopher Creutzig <christopher@creutzig.de>.\n\n    .. versionadded:: 0.8\n    '
    name = 'MuPAD'
    aliases = ['mupad']
    filenames = ['*.mu']
    tokens = {'root':[
      (
       '//.*?$', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '"(?:[^"\\\\]|\\\\.)*"', String),
      (
       '\\(|\\)|\\[|\\]|\\{|\\}', Punctuation),
      (
       '(?x)\\b(?:\n                next|break|end|\n                axiom|end_axiom|category|end_category|domain|end_domain|inherits|\n                if|%if|then|elif|else|end_if|\n                case|of|do|otherwise|end_case|\n                while|end_while|\n                repeat|until|end_repeat|\n                for|from|to|downto|step|end_for|\n                proc|local|option|save|begin|end_proc|\n                delete|frame\n              )\\b', Keyword),
      (
       '(?x)\\b(?:\n                DOM_ARRAY|DOM_BOOL|DOM_COMPLEX|DOM_DOMAIN|DOM_EXEC|DOM_EXPR|\n                DOM_FAIL|DOM_FLOAT|DOM_FRAME|DOM_FUNC_ENV|DOM_HFARRAY|DOM_IDENT|\n                DOM_INT|DOM_INTERVAL|DOM_LIST|DOM_NIL|DOM_NULL|DOM_POLY|DOM_PROC|\n                DOM_PROC_ENV|DOM_RAT|DOM_SET|DOM_STRING|DOM_TABLE|DOM_VAR\n              )\\b', Name.Class),
      (
       '(?x)\\b(?:\n                PI|EULER|E|CATALAN|\n                NIL|FAIL|undefined|infinity|\n                TRUE|FALSE|UNKNOWN\n              )\\b',
       Name.Constant),
      (
       '\\b(?:dom|procname)\\b', Name.Builtin.Pseudo),
      (
       "\\.|,|:|;|=|\\+|-|\\*|/|\\^|@|>|<|\\$|\\||!|\\'|%|~=", Operator),
      (
       '(?x)\\b(?:\n                and|or|not|xor|\n                assuming|\n                div|mod|\n                union|minus|intersect|in|subset\n              )\\b',
       Operator.Word),
      (
       '\\b(?:I|RDN_INF|RD_NINF|RD_NAN)\\b', Number),
      (
       '(?x)\n              ((?:[a-zA-Z_#][\\w#]*|`[^`]*`)\n              (?:::[a-zA-Z_#][\\w#]*|`[^`]*`)*)(\\s*)([(])',
       bygroups(Name.Function, Text, Punctuation)),
      (
       '(?x)\n              (?:[a-zA-Z_#][\\w#]*|`[^`]*`)\n              (?:::[a-zA-Z_#][\\w#]*|`[^`]*`)*', Name.Variable),
      (
       '[0-9]+(?:\\.[0-9]*)?(?:e[0-9]+)?', Number),
      (
       '\\.[0-9]+(?:e[0-9]+)?', Number),
      (
       '.', Text)], 
     'comment':[
      (
       '[^*/]', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)]}


class BCLexer(RegexLexer):
    __doc__ = '\n    A `BC <https://www.gnu.org/software/bc/>`_ lexer.\n\n    .. versionadded:: 2.1\n    '
    name = 'BC'
    aliases = ['bc']
    filenames = ['*.bc']
    tokens = {'root':[
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '"(?:[^"\\\\]|\\\\.)*"', String),
      (
       '[{}();,]', Punctuation),
      (
       words(('if', 'else', 'while', 'for', 'break', 'continue', 'halt', 'return', 'define',
       'auto', 'print', 'read', 'length', 'scale', 'sqrt', 'limits', 'quit', 'warranty'),
         suffix='\\b'), Keyword),
      (
       '\\+\\+|--|\\|\\||&&|([-<>+*%\\^/!=])=?',
       Operator),
      (
       '[0-9]+(\\.[0-9]*)?', Number),
      (
       '\\.[0-9]+', Number),
      (
       '.', Text)], 
     'comment':[
      (
       '[^*/]+', Comment.Multiline),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)]}