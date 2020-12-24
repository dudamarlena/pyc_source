# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/OpenCobolIDE/open_cobol_ide/extlibs/keyring/util/escape.py
# Compiled at: 2016-12-30 07:03:41
# Size of source mod 2**32: 1497 bytes
"""
escape/unescape routines available for backends which need
alphanumeric usernames, services, or other values
"""
import re, string, sys
PY3 = sys.version_info[0] == 3
if PY3:

    def u(s):
        return s


    def _unichr(c):
        return chr(c)


else:

    def u(s):
        return unicode(s, 'unicode_escape')


    def _unichr(c):
        return unichr(c)


LEGAL_CHARS = (getattr(string, 'letters', None) or getattr(string, 'ascii_letters')) + string.digits
ESCAPE_FMT = '_%02X'

def _escape_char(c):
    """Single char escape. Return the char, escaped if not already legal"""
    if isinstance(c, int):
        c = _unichr(c)
    if c in LEGAL_CHARS:
        return c
    return ESCAPE_FMT % ord(c)


def escape(value):
    """
    Escapes given string so the result consists of alphanumeric chars and
    underscore only.
    """
    return ''.join(_escape_char(c) for c in value.encode('utf-8'))


def _unescape_code(regex_match):
    ordinal = int(regex_match.group('code'), 16)
    if sys.version_info >= (3, ):
        return bytes([ordinal])
    return chr(ordinal)


def unescape(value):
    """
    Inverse of escape.
    """
    re_esc = re.compile(ESCAPE_FMT.replace('%02X', '(?P<code>[0-9A-F]{2})').encode('ascii'))
    return re_esc.sub(_unescape_code, value.encode('ascii')).decode('utf-8')