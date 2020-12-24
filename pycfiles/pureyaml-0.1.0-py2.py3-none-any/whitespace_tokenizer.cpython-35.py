# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/tokenizer/whitespace_tokenizer.py
# Compiled at: 2018-08-07 00:24:08
# Size of source mod 2**32: 271 bytes
from .base_tokenizer import BaseTokenizer

class WhitespaceTokenizer(BaseTokenizer):

    def cut(self, sentence):
        splitted_tokens = sentence.split(' ')
        while '_' in splitted_tokens:
            splitted_tokens.remove('_')

        return splitted_tokens