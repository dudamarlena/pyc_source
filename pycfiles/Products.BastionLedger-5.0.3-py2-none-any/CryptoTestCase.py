# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/tests/CryptoTestCase.py
# Compiled at: 2012-03-06 02:26:51
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
ZopeTestCase.installProduct('BastionCrypto')
ZopeTestCase.installProduct('Archetypes')
PloneTestCase.setupPloneSite(products=('BastionCrypto', 'Archetypes'), extension_profiles=[
 'Products.CMFFormController:CMFFormController',
 'Products.CMFQuickInstallerTool:CMFQuickInstallerTool',
 'Products.MimetypesRegistry:MimetypesRegistry',
 'Products.PortalTransforms:PortalTransforms',
 'Products.Archetypes:Archetypes',
 'Products.Archetypes:Archetypes_sampletypes'])

class CryptoTestCase(PloneTestCase.PloneTestCase):
    """ Base test case for testing BastionCallCentre functionality """

    def afterSetUp(self):
        self.portal.manage_addProduct['BastionCrypto'].manage_addBastionPGPKeyZopeRepository()
        self.pks = self.portal.pks