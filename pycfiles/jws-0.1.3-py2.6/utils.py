# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/jws/utils.py
# Compiled at: 2015-03-10 11:52:29
from __future__ import unicode_literals
import base64, json, sys
if sys.version < b'3':
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

def to_bytes_2and3(s):
    if type(s) != binary_type:
        s = bytes(s, b'UTF-8')
    return s


def base64url_decode(input):
    input = to_bytes_2and3(input)
    input += b'=' * (4 - len(input) % 4)
    return base64.urlsafe_b64decode(input)


def base64url_encode(input):
    return base64.urlsafe_b64encode(to_bytes_2and3(input)).replace(b'=', b'')


def to_json(a):
    return json.dumps(a)


def from_json(a):
    return json.loads(a)


def to_base64(a):
    return base64url_encode(a)


def from_base64(a):
    return base64url_decode(a)


def encode(a):
    return to_base64(to_json(a))


def decode(a):
    return from_json(from_base64(a))


def _ord(val):
    if sys.version < b'3':
        return ord(val)
    else:
        return val


def constant_time_compare(val1, val2):
    """
    Returns True if the two strings are equal, False otherwise.

    The time taken is independent of the number of characters that match.

    For the sake of simplicity, this function executes in constant time only
    when the two strings have the same length. It short-circuits when they
    have different lengths.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for (x, y) in zip(val1, val2):
        result |= _ord(x) ^ _ord(y)

    return result == 0