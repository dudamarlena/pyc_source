# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/utils.py
# Compiled at: 2008-08-07 12:43:23
from zope.component import getMultiAdapter
from zope import event
from Products.Archetypes.event import ObjectInitializedEvent
from easyshop.core.interfaces import IOrderManagement

class TestSession:
    """
    """
    __module__ = __name__

    def __init__(self, sid):
        """
        """
        self.sid = sid

    def getId(self):
        """
        """
        return self.sid


def createMember(self, id=None):
    """
    """
    if id is None:
        id = 'newmember'
    self.membership = self.portal_membership
    self.membership.addMember(id, 'secret', ['Member'], [])
    return


def createTestEnvironment(self):
    """
    """
    createMember(self, 'newmember')
    self.invokeFactory('EasyShop2', id='myshop', title='MyShop', description='My test shop')
    event.notify(ObjectInitializedEvent(self.myshop))
    self.shop = self.myshop
    self.shop.at_post_create_script()
    self.shop.setPayPalId('haendler@iqpp.de')
    self.shop.shippingprices.manage_addProduct['easyshop.core'].addShippingPrice(id='default', price=10.0)
    self.shop.shippingprices.default.reindexObject()
    self.shop.paymentprices.manage_addProduct['easyshop.core'].addPaymentPrice(id='default', price=100.0)
    self.shop.setCountries(['Germany'])
    self.shop.products.manage_addProduct['easyshop.core'].addProduct(id='product_1', price=22.0)
    self.product_1 = self.shop.products.product_1
    self.product_1.setWeight(10.0)
    self.product_1.setStockAmount(10.0)
    colors = [{'name': 'Default', 'price': '0.0'}, {'name': 'Red', 'price': '-10.0'}, {'name': 'Blue', 'price': '0.0'}, {'name': 'Green', 'price': '15.0'}]
    colors_for_groups = [{'name': 'Default', 'price': '0.0'}, {'name': 'Red', 'price': '1000.0'}, {'name': 'Blue', 'price': '2000.0'}, {'name': 'Green', 'price': '3000.0'}]
    materials = [{'name': 'Default', 'price': '0.0'}, {'name': 'Iron', 'price': '-100.0'}, {'name': 'Wood', 'price': '0.0'}, {'name': 'Gold', 'price': '150.0'}]
    qualities = [{'name': 'Default', 'price': '0.0'}, {'name': 'Low', 'price': '-1000.0'}, {'name': 'Medium', 'price': '0.0'}, {'name': 'High', 'price': '1500.0'}]
    sizes_for_groups = [{'name': 'Default', 'price': '0.0'}, {'name': 'Small', 'price': '-11.0'}, {'name': 'Medium', 'price': '1.0'}, {'name': 'Large', 'price': '22.0'}]
    self.product_1.invokeFactory('ProductProperty', id='color', title='Color')
    for option in colors:
        self.product_1.color.invokeFactory('ProductPropertyOption', id=option['name'], title=option['name'], price=option['price'])

    self.product_1.invokeFactory('ProductProperty', id='material', title='Material')
    for option in materials:
        self.product_1.material.invokeFactory('ProductPropertyOption', id=option['name'], title=option['name'], price=option['price'])

    self.product_1.invokeFactory('ProductProperty', id='quality', title='Quality')
    for option in qualities:
        self.product_1.quality.invokeFactory('ProductPropertyOption', id=option['name'], title=option['name'], price=option['price'])

    self.shop.products.manage_addProduct['easyshop.core'].addProduct(id='product_2', price=19.0)
    self.product_2 = self.shop.products.product_2
    self.product_2.setWeight(20.0)
    self.product_2.setStockAmount(20.0)
    self.shop.products.manage_addProduct['easyshop.core'].addProduct(id='product_42', price=19.0)
    self.product_42 = self.shop.products.product_42
    self.product_42.setStockAmount(0.0)
    self.shop.groups.invokeFactory('ProductGroup', id='group_1')
    self.shop.groups.invokeFactory('ProductGroup', id='group_2')
    self.group_1 = self.shop.groups.group_1
    self.group_2 = self.shop.groups.group_2
    self.group_1.invokeFactory('ProductProperty', id='color', title='Color')
    for option in colors_for_groups:
        self.group_1.color.invokeFactory('ProductPropertyOption', id=option['name'], title=option['name'], price=option['price'])

    self.group_1.invokeFactory('ProductProperty', id='size', title='Size')
    for option in sizes_for_groups:
        self.group_1.size.invokeFactory('ProductPropertyOption', id=option['name'], title=option['name'], price=option['price'])

    self.group_1.addReference(self.product_1, 'groups_products')
    self.group_1.addReference(self.product_2, 'groups_products')
    self.group_2.addReference(self.product_1, 'groups_products')
    self.shop.manage_addProduct['easyshop.core'].addCategory(id='category_1')
    self.shop.category_1.manage_addProduct['easyshop.core'].addCategory(id='category_11')
    self.shop.category_1.manage_addProduct['easyshop.core'].addCategory(id='category_12')
    self.shop.category_1.category_11.manage_addProduct['easyshop.core'].addCategory(id='category_111')
    self.shop.manage_addProduct['easyshop.core'].addCategory(id='category_2')
    self.shop.manage_addProduct['easyshop.core'].addCategory(id='category_3')
    self.category_1 = self.shop.categories.category_1
    self.category_2 = self.shop.categories.category_2
    self.category_3 = self.shop.categories.category_3
    self.category_1.category_11.setPositionInParent(0)
    self.category_1.category_12.setPositionInParent(1)
    self.category_1.category_11.setParentCategory(self.category_1)
    self.category_1.category_12.setParentCategory(self.category_1)
    self.category_1.category_11.category_111.setParentCategory(self.category_1.category_11)
    self.category_1.category_11.addReference(self.product_1, 'categories_products')
    self.category_1.category_11.addReference(self.product_2, 'categories_products')
    self.category_3.addReference(self.product_42, 'categories_products')
    self.shop.taxes.manage_addProduct['easyshop.core'].addDefaultTax(id='default', rate=19.0)
    self.sid = self.REQUEST.SESSION = TestSession('123')


def createTestOrder(self):
    """
    """
    view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name='addToCart')
    view.addToCart()
    view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name='addToCart')
    view.addToCart()
    om = IOrderManagement(self.shop)
    self.order = om.addOrder()