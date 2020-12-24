# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-jwt/lib/python2.7/site-packages/django_jwt/settings.py
# Compiled at: 2015-12-28 11:05:50
"""django_jwt settings."""
from django.conf import settings
JWT_QUERYSTRING_ARG = getattr(settings, 'JWT_QUERYSTRING_ARG', 'jwt')