# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/settings.py
# Compiled at: 2014-08-09 03:47:51
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
MODELS = getattr(settings, 'PLUGSHOP_MODELS', {})
FORMS = getattr(settings, 'PLUGSHOP_FORMS', {})
CONFIG = getattr(settings, 'PLUGSHOP_CONFIG', {})
OPTIONS = getattr(settings, 'PLUGSHOP_OPTIONS', {})
MESSAGES = getattr(settings, 'PLUGSHOP_MESSAGES', {})
PRODUCT_MODEL_DEFAULT = 'plugshop.Product'
PRODUCT_MODEL = MODELS.get('PRODUCT', PRODUCT_MODEL_DEFAULT)
CATEGORY_MODEL_DEFAULT = 'plugshop.Category'
CATEGORY_MODEL = MODELS.get('CATEGORY', CATEGORY_MODEL_DEFAULT)
ORDER_MODEL_DEFAULT = 'plugshop.Order'
ORDER_MODEL = MODELS.get('ORDER', ORDER_MODEL_DEFAULT)
ORDER_PRODUCTS_MODEL_DEFAULT = 'plugshop.OrderProducts'
ORDER_PRODUCTS_MODEL = MODELS.get('ORDER_PRODUCTS', ORDER_PRODUCTS_MODEL_DEFAULT)
ORDER_FORM_DEFAULT = 'plugshop.forms.OrderForm'
ORDER_FORM = FORMS.get('ORDER', ORDER_FORM_DEFAULT)
REQUEST_NAMESPACE = CONFIG.get('REQUEST_NAMESPACE', 'cart')
SESSION_NAMESPACE = CONFIG.get('SESSION_NAMESPACE', 'cart')
URL_PREFIX = CONFIG.get('URL_PREFIX', '')
STATUS_CHOICES = OPTIONS.get('STATUS_CHOICES', (
 (
  1, _('Created')),
 (
  2, _('Confirmed')),
 (
  3, _('Denied')),
 (
  4, _('Shipped')),
 (
  5, _('Completed'))))
STATUS_CHOICES_START = STATUS_CHOICES[0][0]
STATUS_CHOICES_FINISH = STATUS_CHOICES[(-1)][0]
MESSAGE_SUCCESS = MESSAGES.get('SUCCESS', 'Order created')
MESSAGE_NEW_ORDER_USER = MESSAGES.get('NEW_ORDER_USER', 'New Order')
MESSAGE_NEW_ORDER_ADMIN = MESSAGES.get('NEW_ORDER_ADMIN', 'New Order')