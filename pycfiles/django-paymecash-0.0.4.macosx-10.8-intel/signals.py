# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/signals.py
# Compiled at: 2013-09-17 23:35:42
from django.dispatch import Signal
payment_process = Signal()
payment_completed = Signal()
payment_fail = Signal()