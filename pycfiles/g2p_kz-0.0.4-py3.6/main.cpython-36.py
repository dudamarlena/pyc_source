# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kzphoneme\main.py
# Compiled at: 2019-09-27 07:24:34
# Size of source mod 2**32: 1619 bytes
import re, unicodedata
from nltk import word_tokenize
from kzphoneme.convert import Convert
from kzphoneme.expand import Number
from kzphoneme.normalize import Normalize

class Phoneme(Number, Convert, Normalize):

    def __init__(self, *args, **kwargs):
        (super(Phoneme, self).__init__)(*args, **kwargs)

    def __call__(self, string: str, script='arab'):
        string = string.strip().rstrip()
        string = self.norm(string, script)
        string = self.convert(string, script)
        string = self.normalize_numbers(string)
        text = string.lower()
        text = text.replace('—', '-')
        text = ''.join(char for char in unicodedata.normalize('NFD', text) if unicodedata.category(char) != 'Mn')
        text = re.sub("[^ a-z'.,?!\\-]", '', text)
        text = text.replace('t.b.', 'taci basqa.')
        text = text.replace('t.t.', 'taci tacilar.')
        text = text.replace('t.s.', 'taci sondaylar.')
        text = text.replace('t.s.s.', 'taci sol syaqti.')
        words = word_tokenize(text)
        phonemes = []
        for word in words:
            phs = self._get_phonemes(word)
            [phonemes.append(ph.upper()) for ph in phs]
            phonemes.append(' ')

        return phonemes[:-1]

    @staticmethod
    def _get_phonemes(word: str):
        chars = list(word)
        phonemes = []
        pos = 0
        for i, ch in enumerate(chars):
            if ch == 'h':
                phonemes[(pos - 1)] += 'h'
            else:
                phonemes.append(ch)
                pos += 1

        return phonemes