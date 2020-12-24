# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/test_util.py
# Compiled at: 2019-10-16 18:51:20
# Size of source mod 2**32: 939 bytes
"""
Test the utils lib.
"""
from __future__ import absolute_import
import pytest
from pynsot.util import slugify, validate_cidr

def test_validate_cidr():
    """Test ``validate_cidr()``."""
    assert validate_cidr('0.0.0.0/0')
    assert validate_cidr('1.2.3.4/32')
    assert validate_cidr('::/0')
    assert validate_cidr('fe8::/10')
    assert not validate_cidr('bogus')
    assert not validate_cidr(None)
    assert not validate_cidr(object())
    assert not validate_cidr({})
    assert not validate_cidr([])


def test_slugify():
    cases = [
     ('/', '_'),
     ('my cool string', 'my cool string'),
     ('Ethernet1/2', 'Ethernet1_2'),
     ('foo-bar1:xe-0/0/0.0_foo-bar2:xe-0/0/0.0', 'foo-bar1:xe-0_0_0.0_foo-bar2:xe-0_0_0.0')]
    for case, expected in cases:
        assert slugify(case) == expected