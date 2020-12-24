# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/tests/base.py
# Compiled at: 2008-06-20 09:34:52
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)
from AccessControl.SecurityManagement import newSecurityManager
from transaction import commit
from Products.Five import zcml
from Testing import ZopeTestCase
from Testing.ZopeTestCase.utils import setupCoreSessions
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite
import easyshop.carts
from plone.app import relations
setupCoreSessions()
ZopeTestCase.installProduct('SiteAccess')
ZopeTestCase.installProduct('EasyShop', 'plone.app.relations')
PloneTestCase.setupPloneSite(products=['EasyShop', 'plone.app.relations'])

class EasyShopCartsSite(PloneSite):
    __module__ = __name__

    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        portal = app.plone
        uf = app.acl_users
        user = uf.getUserById(PloneTestCase.portal_owner).__of__(uf)
        newSecurityManager(None, user)
        zcml.load_config('configure.zcml', easyshop.carts)
        zcml.load_config('configure.zcml', relations)
        portal.invokeFactory('EasyShop', 'shop', title='EasyShop')
        portal.portal_workflow.doActionFor(portal.shop, 'publish')
        portal.shop.at_post_create_script()
        portal.shop.products.invokeFactory('Product', 'product', title='Product')
        portal.portal_workflow.doActionFor(portal.shop.products.product, 'publish')
        portal.product = portal.shop.products.product
        commit()
        ZopeTestCase.close(app)
        return


class EasyShopCartsTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__
    layer = EasyShopCartsSite


class EasyShopCartsFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    __module__ = __name__
    layer = EasyShopCartsSite