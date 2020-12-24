# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/tests/test_rules.py
# Compiled at: 2009-01-13 06:18:21
import os, sys, unittest
dirname = os.path.dirname(__file__)
if dirname not in sys.path:
    sys.path.append(os.path.split(dirname)[0])
from ecs.cart.tests import database

class RulesTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


def test_suite():
    tests = [
     unittest.makeSuite(RulesTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    unittest.main()