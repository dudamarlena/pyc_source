# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /projects/devel/opbasm/doc/util/PicoBlazeLexer.py
# Compiled at: 2015-11-17 22:52:16
from pygments.lexer import RegexLexer
from pygments.token import *
from pygments.style import Style
import re

class PicoBlazeLexer(RegexLexer):
    name = 'PicoBlaze'
    aliases = ['pb']
    filenames = ['*.psm', '*.psm4']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '[\\t ]+', Text),
              (
               '[{}]', Punctuation),
              (
               '<.+>', Generic.Emph),
              (
               '[.\\w]+:', Name.Label),
              (
               'pbhex\\(', Name.Builtin, 'pbhex'),
              (
               '\\w+\\(', Name.Builtin, 'macro'),
              (
               '(if|for|do|while) *\\(', Name.Builtin, 'macro'),
              (
               'else', Name.Builtin),
              (
               '[\\w&@]+[#$%]?', Keyword, 'args'),
              (
               ';[\\t ]*pragma.*\\n', Comment.Special),
              (
               ';.*\\n', Comment),
              (
               '.*\\n', Text)], 
       'args': [
              (
               '[\\t ]+', Text),
              (
               '\\w+\\(', Name.Builtin, 'macro'),
              (
               '[,()]', Punctuation),
              (
               "\\[.*\\]'d", Number),
              (
               "\\[.*\\]'b", Number.Bin),
              (
               '\\[.*\\]', Number.Hex),
              (
               "\\d+'d", Number),
              (
               "[01]+'b", Number.Bin),
              (
               '[0-9a-f]+(?!\\w)', Number.Hex),
              (
               '"[^"]"', String.Char),
              (
               '[.\\w]+[#$%]?', Name),
              (
               "'(upper|lower)", Operator),
              (
               ';.*\\n', Comment, '#pop'),
              (
               '.*\\n', Text, '#pop')], 
       'macro': [
               (
                '\\s+', Text),
               (
                'pbhex\\(', Name.Builtin, 'pbhex'),
               (
                '\\w+\\(', Name.Builtin, 'macro'),
               (
                ',', Punctuation),
               (
                '(:=|=:|<<|>>|!=|==|[-+*/~<>])', Operator),
               (
                '0x[0-9a-f]+', Number.Hex),
               (
                '0b[01]+', Number.Bin),
               (
                '\\d+', Number),
               (
                '\\w+', String),
               (
                '[^ ),]+', String),
               (
                '[^;)]*\\)', Name.Builtin, '#pop')], 
       'pbhex': [
               (
                '\\s+', Text),
               (
                ',', Punctuation),
               (
                '[^,)]+', Number.Hex),
               (
                '\\)', Name.Builtin, '#pop')]}


class OptimumTint(Style):
    default_style = ''
    styles = {Text: '#000', 
       Punctuation: '#333', 
       Generic.Emph: 'italic #800', 
       Name: '#000', 
       Name.Label: '#080', 
       Name.Builtin: '#60c', 
       Keyword: 'bold #00c', 
       Comment: '#777', 
       Comment.Special: 'italic #a00', 
       Number: 'bold #088', 
       String.Char: '#c50', 
       Operator: '#980'}