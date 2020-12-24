# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/checkpermission/tests/test_check.py
# Compiled at: 2009-11-06 11:57:19
import unittest
from Products.PloneTestCase.ptc import PloneTestCase
from collective.testcaselayer.ptc import ptc_layer
from zope.component import getMultiAdapter

class CheckPermissionUnit(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.operator = pow

    def tearDown(self):
        self.operator = None
        return

    def test_pow(self):
        self.assertEqual(self.operator(2, 2), 4)


class CheckIntegration(PloneTestCase):
    __module__ = __name__
    layer = ptc_layer

    def test_check_perm(self):
        """ Assert if we can modify a folder """
        view = getMultiAdapter((self.folder, None), name='check_permission')
        self.assertTrue(view.check('Modify portal content'))
        return

    def test_check_anonymous(self):
        """ Anonymous cannot modify a folder """
        self.logout()
        view = getMultiAdapter((self.folder, None), name='check_permission')
        self.assertFalse(view.check('Modify portal content'))
        return


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)