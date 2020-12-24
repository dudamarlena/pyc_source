# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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