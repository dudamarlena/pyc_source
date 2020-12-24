# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/charsetprober.py
# Compiled at: 2018-01-22 17:51:30
from . import constants
import re

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
        aBuf = re.sub('([\x00-\x7f])+', ' ', aBuf)
        return aBuf

    def filter_without_english_letters(self, aBuf):
        aBuf = re.sub('([A-Za-z])+', ' ', aBuf)
        return aBuf

    def filter_with_english_letters(self, aBuf):
        return aBuf