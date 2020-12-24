# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_speedups.py
# Compiled at: 2019-06-26 11:58:00
from twisted.trial.unittest import SkipTest, TestCase
from pyutil.jsonutil import decoder
from pyutil.jsonutil import encoder

class TestSpeedups(TestCase):

    def test_scanstring(self):
        if not encoder.c_encode_basestring_ascii:
            raise SkipTest('no C extension speedups available to test')
        self.assertEqual(decoder.scanstring.__module__, 'simplejson._speedups')
        self.assert_(decoder.scanstring is decoder.c_scanstring)

    def test_encode_basestring_ascii(self):
        if not encoder.c_encode_basestring_ascii:
            raise SkipTest('no C extension speedups available to test')
        self.assertEqual(encoder.encode_basestring_ascii.__module__, 'simplejson._speedups')
        self.assert_(encoder.encode_basestring_ascii is encoder.c_encode_basestring_ascii)