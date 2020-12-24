# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertbanagale/code/opensource/django-address/django-address/example_site/address/apps.py
# Compiled at: 2020-05-10 01:24:31
from django.apps import AppConfig

class AddressConfig(AppConfig):
    """
    Define config for the member app so that we can hook in signals.
    """
    name = 'address'