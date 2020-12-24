# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\lang\polish.py
# Compiled at: 2011-10-24 15:37:01
import re
from droopy import attr, op

class Polish(object):

    @attr
    def lang(self, d):
        return 'pl_PL'

    @attr
    def vowels(self, d):
        return 'aąeęioóuyAĄEĘIOÓUY'

    @attr
    def consonants(self, d):
        return 'bcćdfghjklłmnńpqrsśtvwxzźżBCĆDFGHJKLŁMNŃPQRSŚTVWXZŻŹ'

    @attr
    def bigs(self, d):
        return 'AĄEĘIOÓUYBCĆDFGHJKLŁMNŃPQRSŚTVWXZŻŹ'

    @attr
    def smalls(self, d):
        return 'aąeęioóuybcćdfghjklłmnńpqrsśtvwxzźż'

    @op
    def count_syllables_in_word(self, d, word):
        vowels = len(re.findall('[%s]{1,2}' % d.vowels, word))
        if vowels <= 1:
            syllables = vowels
        else:
            soften_consonants = len(re.findall('[%s]i[%s]' % (d.consonants, d.vowels), word))
            syllables = vowels
        return syllables

    @attr
    def foggy_word_syllables(self, d):
        return 3