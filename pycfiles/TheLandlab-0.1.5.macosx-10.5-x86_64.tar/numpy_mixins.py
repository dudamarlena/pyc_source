# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/testing/numpy_mixins.py
# Compiled at: 2014-09-23 12:37:24
from numpy.testing import assert_array_equal

class NumpyArrayTestingMixIn(object):

    def assertArrayEqual(self, actual, expected):
        try:
            assert_array_equal(actual, expected)
        except AssertionError as error:
            self.fail(error)