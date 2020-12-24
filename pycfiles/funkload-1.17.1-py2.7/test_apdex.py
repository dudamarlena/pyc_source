# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/tests/test_apdex.py
# Compiled at: 2015-05-06 05:03:08
import os, sys, unittest
if os.path.realpath(os.curdir) == os.path.realpath(os.path.dirname(__file__)):
    sys.path.append('../..')
from funkload.apdex import Apdex

class TestApdex(unittest.TestCase):

    def test_sanity(self):
        self.assertEqual(Apdex.T, 1.5)
        self.assertTrue(Apdex.satisfying(0.1))
        self.assertTrue(Apdex.satisfying(1.49))
        self.assertFalse(Apdex.satisfying(1.5))
        self.assertTrue(Apdex.tolerable(1.5))
        self.assertTrue(Apdex.tolerable(5.99))
        self.assertFalse(Apdex.tolerable(6.0))
        self.assertTrue(Apdex.frustrating(6.0))

    def test_100_percent_satisfied(self):
        s, t, f = (10, 0, 0)
        score = Apdex.score(s, t, f)
        self.assertTrue(score == 1.0)
        self.assertTrue(score.label == Apdex.Excellent.label)
        self.assertTrue(Apdex.get_label(score) == Apdex.Excellent.label)

    def test_unacceptable(self):
        s, t, f = (0, 0, 10)
        score = Apdex.score(s, t, f)
        self.assertTrue(score == 0)
        self.assertTrue(score.label == Apdex.Unacceptable.label)
        self.assertTrue(Apdex.get_label(score) == Apdex.Unacceptable.label)


if __name__ == '__main__':
    unittest.main()