# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/signals.py
# Compiled at: 2014-08-09 03:47:51
from django.dispatch import Signal
cart_append = Signal(providing_args=['item', 'price', 'quantity'])
cart_remove = Signal(providing_args=['item', 'quantity'])
cart_empty = Signal()
cart_save = Signal()
order_create = Signal(providing_args=['order', 'request'])