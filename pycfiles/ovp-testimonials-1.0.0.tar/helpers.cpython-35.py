# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/helpers.py
# Compiled at: 2017-04-26 13:43:30
# Size of source mod 2**32: 118 bytes
from django.conf import settings

def get_settings(string='OVP_TESTIMONIALS'):
    return getattr(settings, string, {})