# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_policy.py
# Compiled at: 2011-06-29 14:07:37
from dtest import *
from dtest.util import *

@threshold(50.0)
def test_threshold():

    def tfcn(i):
        assert_equal(i % 2, 0)

    for i in range(100):
        yield (
         tfcn, (i,))