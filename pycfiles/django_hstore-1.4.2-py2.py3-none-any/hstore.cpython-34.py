# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/hstore.py
# Compiled at: 2015-12-07 14:15:11
# Size of source mod 2**32: 299 bytes
from django_hstore.fields import DictionaryField, ReferencesField, SerializedDictionaryField
from django_hstore.managers import HStoreManager
from django_hstore.apps import GEODJANGO_INSTALLED
if GEODJANGO_INSTALLED:
    from django_hstore.managers import HStoreGeoManager