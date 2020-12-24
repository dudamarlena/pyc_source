# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/iqpp/plone/rotating/tests/base.py
# Compiled at: 2008-08-03 13:24:54
from Testing import ZopeTestCase
from transaction import commit
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.CMFCore.utils import getToolByName
from Products.Five import zcml
import iqpp.plone.rotating
setupPloneSite()

class RotatingLayer(PloneSite):
    __module__ = __name__

    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        portal = app.plone
        zcml.load_config('configure.zcml', iqpp.plone.rotating)
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-iqpp.plone.rotating:iqpp.plone.rotating')
        commit()
        ZopeTestCase.close(app)

    @classmethod
    def tearDown(cls):
        pass


class RotatingTestCase(PloneTestCase):
    """Base class for integration tests for the 'iqpp.plone.rotating' product.
    """
    __module__ = __name__
    layer = RotatingLayer


class RotatingFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'iqpp.plone.rotating' product.
    """
    __module__ = __name__
    layer = RotatingLayer