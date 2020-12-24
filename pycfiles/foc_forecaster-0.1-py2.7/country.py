# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/model/country.py
# Compiled at: 2011-12-15 04:09:22
"""
Created on 14. 12. 2011.

@author: kermit
"""

class Country(object):
    """
    __indicators concerning a single country
    """

    def __init__(self, code):
        """
        __code - code of a country
        """
        self.__code = code
        self.__indicators = {}

    def get_code(self):
        return self.__code

    def indicator_codes(self):
        return self.__indicators.keys()

    def get_indicator(self, code):
        return self.__indicators[code]

    def set_indicator(self, code, indicator):
        self.__indicators[code] = indicator

    def del_indicators(self):
        del self.__indicators

    code = property(get_code, None, None, None)