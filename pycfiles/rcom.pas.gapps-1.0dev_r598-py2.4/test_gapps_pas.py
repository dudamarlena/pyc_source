# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcom/pas/gapps/tests/test_gapps_pas.py
# Compiled at: 2008-07-07 17:15:22
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from base import TestCase

def test_suite():
    return unittest.TestSuite([ztc.FunctionalDocFileSuite('README.txt', package='rcom.pas.gapps', test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')