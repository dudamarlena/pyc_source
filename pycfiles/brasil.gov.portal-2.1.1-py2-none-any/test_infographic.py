# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_infographic.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.content.infographic import IInfographic
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility
import unittest

class InfographicTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.infographic = api.content.create(self.portal, 'Infographic', 'infographic')

    def test_adding(self):
        self.assertTrue(IInfographic.providedBy(self.infographic))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Infographic')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Infographic')
        schema = fti.lookupSchema()
        self.assertEqual(schema.getName(), 'plone_0_Infographic')

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Infographic')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IInfographic.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
        self.assertTrue(IExcludeFromNavigation.providedBy(self.infographic))