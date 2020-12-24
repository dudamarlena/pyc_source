# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/health_ophtalmo/tests/test_health_ophtalmo.py
# Compiled at: 2012-07-02 19:01:57
import sys, os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__, '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))
import unittest, trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends

class HealthOphtalmoTestCase(unittest.TestCase):
    """
    Test HealthOphtalmo module.
    """

    def setUp(self):
        trytond.tests.test_tryton.install_module('health_ophtalmo')

    def test0005views(self):
        """
        Test views.
        """
        test_view('health_ophtalmo')

    def test0006depends(self):
        """
        Test depends.
        """
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(HealthOphtalmoTestCase))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())