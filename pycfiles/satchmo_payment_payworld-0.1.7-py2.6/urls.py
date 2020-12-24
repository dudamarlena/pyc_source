# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/satchmo_payment_payworld/urls.py
# Compiled at: 2011-11-03 04:28:20
from django.conf.urls.defaults import patterns
from satchmo_store.shop.satchmo_settings import get_satchmo_setting
ssl = get_satchmo_setting('SSL', default_value=False)
urlpatterns = patterns('', (
 '^$', 'satchmo_payment_payworld.views.pay_ship_info', {'SSL': ssl}, 'SATCHMO_PAYMENT_PAYWORLD_satchmo_checkout-step2'), (
 '^confirm/$', 'satchmo_payment_payworld.views.confirm_info', {'SSL': ssl}, 'SATCHMO_PAYMENT_PAYWORLD_satchmo_checkout-step3'), (
 '^success/$', 'satchmo_payment_payworld.views.success', {'SSL': ssl}, 'SATCHMO_PAYMENT_PAYWORLD_satchmo_checkout-success'), (
 '^failure/$', 'satchmo_payment_payworld.views.failure', {'SSL': ssl}, 'SATCHMO_PAYMENT_PAYWORLD_satchmo_checkout-failure'), (
 '^ipn/$', 'satchmo_payment_payworld.views.ipn', {'SSL': ssl}, 'SATCHMO_PAYMENT_PAYWORLD_satchmo_checkout-ipn'), (
 '^confirmorder/$', 'payment.views.confirm.confirm_free_order', {'SSL': ssl, 'key': 'PAYWORLD'}, 'SATCHMO_PAYMENT_PAYWORLD_satchmo_checkout_free-confirm'))