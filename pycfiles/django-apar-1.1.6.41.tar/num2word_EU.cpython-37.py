# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/formattings/num2words/num2word_EU.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1776 bytes
"""
Module: num2word_EU.py
Requires: num2word_base.py
Version: 1.1

Author:
   Taro Ogawa (tso@users.sourceforge.org)
   
Copyright:
    Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.

Licence:
    This module is distributed under the Lesser General Public Licence.
    http://www.opensource.org/licenses/lgpl-license.php

Data from:
    http://www.uni-bonn.de/~manfear/large.php

History:
    1.1: add to_currency()
"""
from .num2word_base import Num2Word_Base

class Num2Word_EU(Num2Word_Base):

    def set_high_numwords(self, high):
        max = 3 + 6 * len(high)
        for word, n in zip(high, list(range(max, 3, -6))):
            self.cards[10 ** n] = word + 'یارد'
            self.cards[10 ** (n - 3)] = word + 'یلیون'

    def set_high_numwords_str(self, high):
        max = 3 + 6 * len(high)
        for word, n in zip(high, list(range(max, 3, -6))):
            self.cards_str[10 ** n] = word + 'یارد'
            self.cards_str[10 ** (n - 3)] = word + 'یلیون'

    def base_setup(self):
        lows = ['نون', 'اکت', 'سپت', 'سکست', 'کوینت', 'کوادر', 'تر', '', '']
        units = ['', 'un', 'duo', 'tre', 'quattuor', 'quin', 'sex', 'sept',
         'octo', 'novem']
        tens = ['dec', 'vigint', 'trigint', 'quadragint', 'quinquagint',
         'sexagint', 'septuagint', 'octogint', 'nonagint']
        self.high_numwords = ['cent'] + self.gen_high_numwords(units, tens, lows)
        self.high_numwords_str = ['cent'] + self.gen_high_numwords(units, tens, lows)

    def to_currency(self, val, longval=True, jointxt=''):
        return self.to_splitnum(val, hightxt='Euro/s', lowtxt='Euro cent/s', jointxt=jointxt,
          longval=longval)