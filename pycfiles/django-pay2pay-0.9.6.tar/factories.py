# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-pay2pay/pay2pay/factories.py
# Compiled at: 2013-06-30 04:02:46
import factory
from .models import Payment

class PaymentF(factory.Factory):
    FACTORY_FOR = Payment