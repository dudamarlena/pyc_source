# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/tests/tests.py
# Compiled at: 2009-03-31 04:47:32
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from quintagroup.pingtool.config import PROJECTNAME
from base import FunctionalTestCase

def test_suite():
    return unittest.TestSuite([doctestunit.DocTestSuite(module='%s.PingTool' % PROJECTNAME, setUp=testing.setUp, tearDown=testing.tearDown), ztc.FunctionalDocFileSuite('browser.txt', package='%s.tests' % PROJECTNAME, test_class=FunctionalTestCase)])