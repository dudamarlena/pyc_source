# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/demo/sparkle/models/compat.py
# Compiled at: 2015-04-11 12:36:40
# Size of source mod 2**32: 239 bytes
try:
    from django.db.models import GenericIPAddressField
except ImportError:
    from django.db.models import IPAddressField as GenericIPAddressField