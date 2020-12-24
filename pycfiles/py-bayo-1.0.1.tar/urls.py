# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/satchmo_payment/urls.py
# Compiled at: 2008-01-28 09:29:01
from django.conf.urls.defaults import *
from satchmo.configuration import config_get_group
import views
config = config_get_group('PAYMENT_BANKPASSWEB')
urlpatterns = patterns('satchmo', (
 '^$', views.pay_ship_info, {'SSL': config.SSL.value}, 'BANKPASSWEB_satchmo_checkout-step2'), (
 '^confirm/$', views.confirm_info, {'SSL': config.SSL.value}, 'BANKPASSWEB_satchmo_checkout-step3'), (
 '^success/$', views.success, {'SSL': config.SSL.value}, 'BANKPASSWEB_satchmo_checkout-success'), (
 '^ipn/$', views.ipn, {'SSL': config.SSL.value}, 'BANKPASSWEB_satchmo_checkout-ipn'))