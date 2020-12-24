# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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