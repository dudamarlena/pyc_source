# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\upxer\UtilPytxer.py
# Compiled at: 2018-01-11 14:23:14
# Size of source mod 2**32: 442 bytes
import re
regex_has_some_number = re.compile('(\\d)')
regex_has_some_letter = re.compile('([A-z])')
regex_is_valid_email = re.compile('^[^\\.,,][\\w+!]+@(?:[A-z0-9]+\\.)+[A-z]{1,6}$')

def has_some_number(text):
    return bool(regex_has_some_number.search(text))


def has_some_letter(text):
    return bool(regex_has_some_letter.search(text))


def is_valid_email(email):
    return bool(regex_is_valid_email.search(email))