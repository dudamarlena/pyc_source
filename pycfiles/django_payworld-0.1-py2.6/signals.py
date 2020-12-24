# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_payworld/signals.py
# Compiled at: 2012-02-15 01:02:17
import django.dispatch
payment_notification = django.dispatch.Signal(providing_args=[
 'transaction_id',
 'order_id',
 'order_total',
 'payer_email',
 'seller_name',
 'shop_id'])
payment_error = django.dispatch.Signal(providing_args=[
 'transaction_id',
 'order_id',
 'order_total',
 'payer_email',
 'seller_name',
 'shop_id',
 'hash'])