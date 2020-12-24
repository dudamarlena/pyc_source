# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/borg/supergroup/tests.py
# Compiled at: 2008-04-05 07:47:21
import unittest, doctest
from zope.interface import implements
from zope.app.testing import placelesssetup
import zope.testing.doctest
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
import borg.supergroup

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', borg.supergroup)
    fiveconfigure.debug_mode = False
    ztc.installPackage('borg.supergroup')


setup_product()
ptc.setupPloneSite(products=['borg.supergroup'])

def test_suite():
    suite = []
    suite.extend([ztc.ZopeDocFileSuite('integration.txt', package='borg.supergroup', test_class=ptc.FunctionalTestCase, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)])
    suite.extend([zope.testing.doctest.DocTestSuite(borg.supergroup.plugin, setUp=placelesssetup.setUp(), tearDown=placelesssetup.tearDown())])
    return unittest.TestSuite(suite)