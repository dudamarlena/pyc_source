# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/signals.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 2838 bytes
from django.dispatch import Signal
check_student_info = Signal(providing_args=['instance', 'formData', 'request', 'registration'])
post_student_info = Signal(providing_args=['registration'])
request_discounts = Signal(providing_args=['registration'])
apply_discount = Signal(providing_args=['registration', 'discount', 'discount_amount'])
apply_addons = Signal(providing_args=['registration'])
apply_price_adjustments = Signal(providing_args=['registration', 'initial_price'])
post_registration = Signal(providing_args=['registration'])
get_customer_data = Signal(providing_args=['customer'])