# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/config.py
# Compiled at: 2008-08-06 16:25:07
import os
from Globals import package_home
from Products.CMFCore.permissions import setDefaultRoles
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('EasyShop')
PROJECTNAME = 'easyshop.shop'
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {'Customer': 'EasyShop: Add Customer', 'Address': 'EasyShop: Add Address', 'EasyShop': 'EasyShop: Add EasyShop'}
setDefaultRoles('EasyShop: Add Customer', ('Manager', ))
product_globals = globals()
home = package_home(product_globals)
DEFAULT_SHOP_FORM = os.path.sep.join([home, 'browser', 'default_shop_form.pt'])
MESSAGES = {'CART_ADDED_PRODUCT': 'The product has been added to the cart.', 'CART_INCREASED_AMOUNT': 'The amount of the product has been increased.', 'ORDER_RECEIVED': 'Your order has been received. Thank you!', 'NO_PRODUCTS_FOUND': 'No products found.', 'VARIANT_ADDED': 'Variant has been added.', 'VARIANT_ALREADY_EXISTS': 'Variant already exists.', 'VARIANTS_DELETED': 'Variant(s) deleted.', 'VARIANTS_SAVED': 'Variant(s) saved.', 'VARIANT_DONT_EXIST': 'The selected combination of properties is not available.', 'PROPERTY_OPTIONS_SAVED': 'Option(s) saved.', 'ADDED_PRODUCT_PROPERTY': 'Property has been added', 'ADDED_PRODUCT_OPTION': 'Option has been added', 'CATEGORY_ALREADY_EXISTS': _('The category aleady exits.'), 'ADDED_CATEGORY': _('The category has been added.'), 'DELETED_CATEGORIES': _('Categories have been deleted.'), 'SELECTED_CATEGORIES': _('Categories have been selected.'), 'MOVED_CATEGORIES': _('Categories have been moved.'), 'DESELECT_CATEGORIES': _('Categories have been deselected.')}
IMAGE_SIZES = {'large': (768, 768), 'preview': (400, 400), 'mini': (200, 200), 'thumb': (128, 128), 'tile': (64, 64), 'icon': (32, 32), 'listing': (16, 16)}
TITLES = (
 ('title', 'Title'), ('short_title', 'Short Title'))
TEXTS = (
 ('none', 'None'), ('description', 'Description'), ('short_text', 'Short Text'), ('text', 'Long Text'))
CURRENCIES = {'euro': {'long': 'Euro', 'short': 'EUR', 'symbol': '€'}, 'usd': {'long': 'US-Dollar', 'short': 'USD', 'symbol': '$'}}
REDO_PAYMENT_STATES = [
 'pending', 'sent (not payed)']
REDO_PAYMENT_PAYMENT_METHODS = [
 'paypal']
CREDIT_CARDS_CHOICES = {_('Visa'): 'Visa', _('MasterCard/EuroCard'): 'MasterCard/EuroCard', _('American Express'): 'American Express'}
CREDIT_CARD_MONTHS_CHOICES = (
 ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'))
CREDIT_CARD_YEARS_CHOICES = (
 ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'))
DEFAULT_COUNTRIES = ('Germany', )
DELIVERY_TIMES_MIN = (
 ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'))
DELIVERY_TIMES_MAX = (
 ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'))
DELIVERY_TIMES_UNIT = (
 (
  'Days', _('Days')), ('Weeks', _('Weeks')))
PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'