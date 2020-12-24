# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_tests.py
# Compiled at: 2011-04-14 13:45:29
from dtest import *
from dtest.util import *

def test_nothing():
    pass


def test_attribute_missing():
    with assert_raises(AttributeError):
        dummy = test_nothing._dt_dtest.missing_attr