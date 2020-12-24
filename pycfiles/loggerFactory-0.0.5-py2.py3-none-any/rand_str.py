# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/loggerFactory-project/loggerFactory/rand_str.py
# Compiled at: 2019-03-01 10:46:21
import string, random

class Charset(object):
    ALPHA_LOWER = string.ascii_lowercase
    ALPHA_UPPER = string.ascii_uppercase
    ALPHA = string.ascii_letters
    HEX = '0123456789abcdef'
    ALPHA_DIGITS = string.ascii_letters + string.digits
    PUNCTUATION = string.punctuation


def rand_str(charset, length=32):
    """
    Generate random string.
    """
    return ('').join([ random.choice(charset) for _ in range(length) ])