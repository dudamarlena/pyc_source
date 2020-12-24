# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/pkg/fuzzywuzzy/string_processing.py
# Compiled at: 2018-09-29 23:45:54
# Size of source mod 2**32: 780 bytes
from __future__ import unicode_literals
import re, string, sys
PY3 = sys.version_info[0] == 3
if PY3:
    string = str

class StringProcessor(object):
    __doc__ = '\n    This class defines method to process strings in the most\n    efficient way. Ideally all the methods below use unicode strings\n    for both input and output.\n    '
    regex = re.compile('(?ui)\\W')

    @classmethod
    def replace_non_letters_non_numbers_with_whitespace(cls, a_string):
        """
        This function replaces any sequence of non letters and non
        numbers with a single white space.
        """
        return cls.regex.sub(' ', a_string)

    strip = staticmethod(string.strip)
    to_lower_case = staticmethod(string.lower)
    to_upper_case = staticmethod(string.upper)