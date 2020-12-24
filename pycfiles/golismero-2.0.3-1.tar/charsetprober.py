# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/charsetprober.py
# Compiled at: 2013-12-09 06:41:17
import constants, re

class CharSetProber:

    def __init__(self):
        pass

    def reset(self):
        self._mState = constants.eDetecting

    def get_charset_name(self):
        return

    def feed(self, aBuf):
        pass

    def get_state(self):
        return self._mState

    def get_confidence(self):
        return 0.0

    def filter_high_bit_only(self, aBuf):
        aBuf = re.sub('([\\x00-\\x7F])+', ' ', aBuf)
        return aBuf

    def filter_without_english_letters(self, aBuf):
        aBuf = re.sub('([A-Za-z])+', ' ', aBuf)
        return aBuf

    def filter_with_english_letters(self, aBuf):
        return aBuf