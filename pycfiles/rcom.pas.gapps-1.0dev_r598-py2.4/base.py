# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcom/pas/gapps/tests/base.py
# Compiled at: 2008-07-07 17:14:30
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from rcom.pas.gapps.config import *
ptc.setupPloneSite()
import rcom.pas.gapps

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', rcom.pas.gapps)
            fiveconfigure.debug_mode = False
            try:
                from Products.Five import pythonproducts
                pythonproducts.setupPythonProducts(None)
                ztc.installProduct(PROJECTNAME)
            except ImportError:
                ztc.installPackage(PROJECTNAME)

            return

        @classmethod
        def tearDown(cls):
            pass