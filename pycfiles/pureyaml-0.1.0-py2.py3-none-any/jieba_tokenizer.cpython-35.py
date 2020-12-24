# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/tokenizer/jieba_tokenizer.py
# Compiled at: 2018-08-07 00:24:03
# Size of source mod 2**32: 1105 bytes
import os.path
from jieba import Tokenizer, setLogLevel
from .base_tokenizer import BaseTokenizer

class JiebaTokenizer(BaseTokenizer):

    def __init__(self):
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        setLogLevel(0)
        self.tokenizer = Tokenizer()
        self.tokenizer.set_dictionary(os.path.join(file_dir, 'dict.txt.big.txt'))
        specific_tokens = [
         '_url_',
         '_num_',
         '_phone_',
         '_time_']
        self.add_words(specific_tokens)

    def cut(self, sentence):
        splitted_tokens = self.tokenizer.lcut(sentence)
        while '_' in splitted_tokens:
            splitted_tokens.remove('_')

        return splitted_tokens

    def add_word(self, word, freq=None, tag=None):
        self.tokenizer.add_word(word, freq, tag)
        self.tokenizer.suggest_freq(word, tune=True)

    def add_words(self, words, freq=None, tag=None):
        for word in words:
            self.add_word(word, freq, tag)