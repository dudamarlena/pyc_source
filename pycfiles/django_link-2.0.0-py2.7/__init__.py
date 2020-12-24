# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/__init__.py
# Compiled at: 2017-07-06 07:47:29
from django.conf import settings
SETTINGS = getattr(settings, 'LINK', {'excluded-viewname-choices': ['admin']})