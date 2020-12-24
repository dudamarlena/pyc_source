# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\st_common.py
# Compiled at: 2013-03-13 13:15:35
"""Common functions for SelfTest modules"""
__revision__ = '$Id$'
import unittest, binascii, sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
from Crypto.Util.py3compat import *

class _list_testloader(unittest.TestLoader):
    suiteClass = list


def list_test_cases(class_):
    """Return a list of TestCase instances given a TestCase class

    This is useful when you have defined test* methods on your TestCase class.
    """
    return _list_testloader().loadTestsFromTestCase(class_)


def strip_whitespace(s):
    """Remove whitespace from a text or byte string"""
    if isinstance(s, str):
        return b(('').join(s.split()))
    else:
        return b('').join(s.split())


def a2b_hex(s):
    """Convert hexadecimal to binary, ignoring whitespace"""
    return binascii.a2b_hex(strip_whitespace(s))


def b2a_hex(s):
    """Convert binary to hexadecimal"""
    return binascii.b2a_hex(s)