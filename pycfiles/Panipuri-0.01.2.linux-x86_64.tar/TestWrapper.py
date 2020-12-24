# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/test/TestWrapper.py
# Compiled at: 2014-04-27 07:55:56
import unittest
from panipuri import *
import tempfile, shutil, os

class TestSimpleWrapper(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp(dir='/tmp')
        self.cache = DBMCache(os.path.join(self.dir, 'testdbmcache'))

    def test_simple_cache(self):
        times_called = {}

        @simple_cache(self.cache)
        def f(x):
            times_called[x] = times_called.get(x, 0) + 1
            return x

        self.assertEqual(f('foo'), 'foo')
        self.assertEqual(f('foo'), 'foo')
        self.assertEqual(f('bar'), 'bar')
        self.assertEqual(f('bar'), 'bar')
        self.assertEqual(times_called['foo'], 1)
        self.assertEqual(times_called['bar'], 1)

    def tearDown(self):
        self.cache.close()
        shutil.rmtree(self.dir)


if __name__ == '__main__':
    unittest.main()