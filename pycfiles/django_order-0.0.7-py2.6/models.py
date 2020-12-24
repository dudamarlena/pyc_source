# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/order/models.py
# Compiled at: 2011-09-15 03:14:50
from django.conf import settings
from order.utils import create_order_classes
if getattr(settings, 'ORDERABLE_MODELS', None):
    for (label, fields) in settings.ORDERABLE_MODELS.items():
        create_order_classes(label, fields)