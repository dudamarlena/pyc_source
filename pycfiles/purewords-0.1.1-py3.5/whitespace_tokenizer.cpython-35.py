# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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