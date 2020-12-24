# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/test/test_sut.py
# Compiled at: 2011-09-29 18:04:04
import unittest
from nose.tools import ok_, assert_false
from sample_sut import sut
from grandma.grandma import t_ways

def test_sut():
    """Use grandma to test the SUT."""
    data = {'p1': [
            'v1_1', 'v1_2', 'v1_3'], 
       'p2': [
            'v2_1', 'v2_2', 'v2_3', 'v2_4'], 
       'p3': [
            'v3_1', 'v3_2', 'v3_3', 'v3_4', 'v3_5']}
    constraints = []
    tests = t_ways(data, 3)
    for t in tests:
        ok_(sut(**t), '%s test failed!' % t)


def test_negative_sut():
    """Use grandma to test the SUT."""
    assert_false(sut('x', 'y', 'z'))