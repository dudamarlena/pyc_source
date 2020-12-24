# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/ezhil.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 2991 bytes
"""
    pygments.lexers.ezhil
    ~~~~~~~~~~~~~~~~~~~~~

    Pygments lexers for Ezhil language.
    
    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, words
from pygments.token import Keyword, Text, Comment, Name
from pygments.token import String, Number, Punctuation, Operator
__all__ = [
 'EzhilLexer']

class EzhilLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Ezhil, a Tamil script-based programming language <http://ezhillang.org>`_\n\n    .. versionadded:: 2.1\n    '
    name = 'Ezhil'
    aliases = ['ezhil']
    filenames = ['*.n']
    mimetypes = ['text/x-ezhil']
    flags = re.MULTILINE | re.UNICODE
    _TALETTERS = '[a-zA-Z_]|[\u0b80-\u0bff]'
    tokens = {'root': [
              include('keywords'),
              (
               '#.*\\n', Comment.Single),
              (
               '[@+/*,^\\-%]|[!<>=]=?|&&?|\\|\\|?', Operator),
              (
               'இல்', Operator.Word),
              (
               words(('assert', 'max', 'min', 'நீளம்', 'சரம்_இடமாற்று', 'சரம்_கண்டுபிடி', 'பட்டியல்',
       'பின்இணை', 'வரிசைப்படுத்து', 'எடு', 'தலைகீழ்', 'நீட்டிக்க', 'நுழைக்க', 'வை',
       'கோப்பை_திற', 'கோப்பை_எழுது', 'கோப்பை_மூடு', 'pi', 'sin', 'cos', 'tan',
       'sqrt', 'hypot', 'pow', 'exp', 'log', 'log10min', 'max', 'exit'), suffix='\\b'), Name.Builtin),
              (
               '(True|False)\\b', Keyword.Constant),
              (
               '[^\\S\\n]+', Text),
              include('identifier'),
              include('literal'),
              (
               '[(){}\\[\\]:;.]', Punctuation)], 
     
     'keywords': [
                  (
                   'பதிப்பி|தேர்ந்தெடு|தேர்வு|ஏதேனில்|ஆனால்|இல்லைஆனால்|இல்லை|ஆக|ஒவ்வொன்றாக|இல்|வரை|செய்|முடியேனில்|பின்கொடு|முடி|நிரல்பாகம்|தொடர்|நிறுத்து|நிரல்பாகம்', Keyword)], 
     
     'identifier': [
                    (
                     '(?:' + _TALETTERS + ')(?:[0-9]|' + _TALETTERS + ')*', Name)], 
     
     'literal': [
                 (
                  '".*?"', String),
                 (
                  '(?u)\\d+((\\.\\d*)?[eE][+-]?\\d+|\\.\\d*)', Number.Float),
                 (
                  '(?u)\\d+', Number.Integer)]}

    def __init__(self, **options):
        super(EzhilLexer, self).__init__(**options)
        self.encoding = options.get('encoding', 'utf-8')