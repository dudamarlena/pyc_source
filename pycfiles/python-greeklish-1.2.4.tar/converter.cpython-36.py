# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marseltzatzo/01.PROJECTS/01.Python/greeklish/greeklish/converter.py
# Compiled at: 2017-04-03 08:22:42
# Size of source mod 2**32: 1019 bytes
from .reverse_stemmer import ReverseStemmer
from .generator import Generator

class Converter(object):
    GREEK_CHARACTERS = 'αβγδεζηθικλμνξοπρσςτυφχψω'

    def __init__(self, max_expansions, generate_greek_variants):
        self.greek_words = []
        self.reverse_stemmer = ReverseStemmer()
        self.generator = Generator(max_expansions)
        self.generate_greek_variants = generate_greek_variants

    def convert(self, input_token):
        if not self.is_greek_word(input_token):
            return
        else:
            if self.generate_greek_variants:
                self.greek_words = self.reverse_stemmer.generate_greek_variants(input_token)
            else:
                self.greek_words.append(input_token)
            return self.generator.generate_greeklish_words(self.greek_words)

    def is_greek_word(self, input_token):
        for char in input_token:
            if char not in self.GREEK_CHARACTERS:
                return False

        return True