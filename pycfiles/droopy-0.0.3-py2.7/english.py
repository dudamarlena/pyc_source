# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\lang\english.py
# Compiled at: 2011-10-24 12:28:56
import re
from droopy import attr, op
from en_syllables_cmudict import SYLLABLES

class English(object):

    @attr
    def lang(self, d):
        return 'en_EN'

    @attr
    def vowels(self, d):
        return 'aeiouyAEIOUY'

    @attr
    def consonants(self, d):
        return 'bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ'

    @attr
    def bigs(self, d):
        return 'AEIOUYBCDFGHJKLMNPQRSTVWXZ'

    @attr
    def smalls(self, d):
        return 'aeiouybcdfghjklmnpqrstvwxz'

    @op
    def count_syllables_in_word(self, d, word):
        return SYLLABLES.get(word.lower(), len(re.findall('[%s]' % d.vowels, word)))

    @attr
    def foggy_word_syllables(self, d):
        return 2