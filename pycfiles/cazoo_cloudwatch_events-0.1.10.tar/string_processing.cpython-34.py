# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\cazipcode-project\cazipcode\pkg\fuzzywuzzy\string_processing.py
# Compiled at: 2017-07-13 17:04:39
# Size of source mod 2**32: 780 bytes
from __future__ import unicode_literals
import re, string, sys
PY3 = sys.version_info[0] == 3
if PY3:
    string = str

class StringProcessor(object):
    """StringProcessor"""
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