# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/test_guid.py
# Compiled at: 2011-03-19 21:05:04
import time, unittest
from chula import guid

class Test_guid(unittest.TestCase):
    doctest = guid

    def msg(self):
        msg = 'Guid generation was too slow: %s ms > %s ms'
        return msg % (round(self.speed / self.tests, 5),
         self.max)

    def fast_enough(self):
        return self.speed / self.tests < self.max

    def unique(self, max=50):
        unique = set()
        for x in xrange(max):
            unique.add(guid.guid())

        return len(unique)

    def setUp(self):
        self.start = time.time()
        self.max = 0.0005
        self.uv = 'Unique violation: guid() generated a non unique guid!'

    def test_guid_length_is_64_characters(self):
        self.assertEquals(len(guid.guid()), 64)

    def test_500(self):
        self.tests = 500
        self.assertEqual(self.tests, self.unique(self.tests), self.uv)
        self.speed = time.time() - self.start
        self.assertTrue(self.fast_enough(), self.msg())

    def test_5000(self):
        self.tests = 5000
        self.assertEqual(self.tests, self.unique(self.tests), self.uv)
        self.speed = time.time() - self.start
        self.assertTrue(self.fast_enough(), self.msg())