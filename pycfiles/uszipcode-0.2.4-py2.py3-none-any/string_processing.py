# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/pkg/fuzzywuzzy/string_processing.py
# Compiled at: 2018-09-29 23:45:54
from __future__ import unicode_literals
import re, string, sys
PY3 = sys.version_info[0] == 3
if PY3:
    string = str

class StringProcessor(object):
    """
    This class defines method to process strings in the most
    efficient way. Ideally all the methods below use unicode strings
    for both input and output.
    """
    regex = re.compile(b'(?ui)\\W')

    @classmethod
    def replace_non_letters_non_numbers_with_whitespace(cls, a_string):
        """
        This function replaces any sequence of non letters and non
        numbers with a single white space.
        """
        return cls.regex.sub(b' ', a_string)

    strip = staticmethod(string.strip)
    to_lower_case = staticmethod(string.lower)
    to_upper_case = staticmethod(string.upper)