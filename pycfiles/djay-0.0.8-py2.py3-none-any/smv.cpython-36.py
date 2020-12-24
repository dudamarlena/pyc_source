# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/smv.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2802 bytes
"""
    pygments.lexers.smv
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the SMV languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Generic, Keyword, Name, Number, Operator, Punctuation, Text
__all__ = [
 'NuSMVLexer']

class NuSMVLexer(RegexLexer):
    __doc__ = '\n    Lexer for the NuSMV language.\n\n    .. versionadded:: 2.2\n    '
    name = 'NuSMV'
    aliases = ['nusmv']
    filenames = ['*.smv']
    mimetypes = []
    tokens = {'root': [
              (
               '(?s)\\/\\-\\-.*?\\-\\-/', Comment),
              (
               '--.*\\n', Comment),
              (
               words(('MODULE', 'DEFINE', 'MDEFINE', 'CONSTANTS', 'VAR', 'IVAR', 'FROZENVAR', 'INIT',
       'TRANS', 'INVAR', 'SPEC', 'CTLSPEC', 'LTLSPEC', 'PSLSPEC', 'COMPUTE', 'NAME',
       'INVARSPEC', 'FAIRNESS', 'JUSTICE', 'COMPASSION', 'ISA', 'ASSIGN', 'CONSTRAINT',
       'SIMPWFF', 'CTLWFF', 'LTLWFF', 'PSLWFF', 'COMPWFF', 'IN', 'MIN', 'MAX', 'MIRROR',
       'PRED', 'PREDICATES'),
                 suffix='(?![\\w$#-])'),
               Keyword.Declaration),
              (
               'process(?![\\w$#-])', Keyword),
              (
               words(('array', 'of', 'boolean', 'integer', 'real', 'word'), suffix='(?![\\w$#-])'), Keyword.Type),
              (
               words(('case', 'esac'), suffix='(?![\\w$#-])'), Keyword),
              (
               words(('word1', 'bool', 'signed', 'unsigned', 'extend', 'resize', 'sizeof', 'uwconst',
       'swconst', 'init', 'self', 'count', 'abs', 'max', 'min'),
                 suffix='(?![\\w$#-])'),
               Name.Builtin),
              (
               words(('EX', 'AX', 'EF', 'AF', 'EG', 'AG', 'E', 'F', 'O', 'G', 'H', 'X', 'Y', 'Z',
       'A', 'U', 'S', 'V', 'T', 'BU', 'EBF', 'ABF', 'EBG', 'ABG', 'next', 'mod',
       'union', 'in', 'xor', 'xnor'),
                 suffix='(?![\\w$#-])'),
               Operator.Word),
              (
               words(('TRUE', 'FALSE'), suffix='(?![\\w$#-])'), Keyword.Constant),
              (
               '[a-zA-Z_][\\w$#-]*', Name.Variable),
              (
               ':=', Operator),
              (
               '[-&|+*/<>!=]', Operator),
              (
               '\\-?\\d+\\b', Number.Integer),
              (
               '0[su][bB]\\d*_[01_]+', Number.Bin),
              (
               '0[su][oO]\\d*_[0-7_]+', Number.Oct),
              (
               '0[su][dD]\\d*_[\\d_]+', Number.Dec),
              (
               '0[su][hH]\\d*_[\\da-fA-F_]+', Number.Hex),
              (
               '\\s+', Text.Whitespace),
              (
               '[()\\[\\]{};?:.,]', Punctuation)]}