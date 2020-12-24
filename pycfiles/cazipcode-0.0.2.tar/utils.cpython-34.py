# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\cazipcode-project\cazipcode\pkg\fuzzywuzzy\utils.py
# Compiled at: 2017-07-13 17:04:39
# Size of source mod 2**32: 2421 bytes
from __future__ import unicode_literals
import sys, functools
from .string_processing import StringProcessor
PY3 = sys.version_info[0] == 3

def validate_string(s):
    """
    Check input has length and that length > 0

    :param s:
    :return: True if len(s) > 0 else False
    """
    try:
        return len(s) > 0
    except TypeError:
        return False


def check_for_none(func):

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if args[0] is None or args[1] is None:
            return 0
        return func(*args, **kwargs)

    return decorator


def check_empty_string(func):

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) == 0 or len(args[1]) == 0:
            return 0
        return func(*args, **kwargs)

    return decorator


bad_chars = str('').join([chr(i) for i in range(128, 256)])
if PY3:
    translation_table = dict((ord(c), None) for c in bad_chars)
    unicode = str

def asciionly(s):
    if PY3:
        return s.translate(translation_table)
    else:
        return s.translate(None, bad_chars)


def asciidammit(s):
    if type(s) is str:
        return asciionly(s)
    else:
        if type(s) is unicode:
            return asciionly(s.encode('ascii', 'ignore'))
        return asciidammit(unicode(s))


def make_type_consistent(s1, s2):
    """If both objects aren't either both string or unicode instances force them to unicode"""
    if isinstance(s1, str) and isinstance(s2, str):
        return (s1, s2)
    else:
        if isinstance(s1, unicode) and isinstance(s2, unicode):
            return (s1, s2)
        return (
         unicode(s1), unicode(s2))


def full_process(s, force_ascii=False):
    """Process string by
        -- removing all but letters and numbers
        -- trim whitespace
        -- force to lower case
        if force_ascii == True, force convert to ascii"""
    if s is None:
        return ''
    if force_ascii:
        s = asciidammit(s)
    string_out = StringProcessor.replace_non_letters_non_numbers_with_whitespace(s)
    string_out = StringProcessor.to_lower_case(string_out)
    string_out = StringProcessor.strip(string_out)
    return string_out


def intr(n):
    """Returns a correctly rounded integer"""
    return int(round(n))