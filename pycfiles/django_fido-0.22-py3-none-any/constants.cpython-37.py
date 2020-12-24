# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/constants.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 557 bytes
"""
Django FIDO constants.

Session key to store FIDO2 requests: FIDO2_REQUEST_SESSION_KEY

Session key to store user PK for django fido authentication
 * AUTHENTICATION_USER_SESSION_KEY

FIDO 2 request type identifiers:
 * FIDO2_REGISTRATION_REQUEST
 * FIDO2_AUTHENTICATION_REQUEST
These are shared between code and JS.
"""
from __future__ import unicode_literals
FIDO2_REQUEST_SESSION_KEY = 'fido2_request'
AUTHENTICATION_USER_SESSION_KEY = 'django_fido_user'
FIDO2_REGISTRATION_REQUEST = 'registration'
FIDO2_AUTHENTICATION_REQUEST = 'authentication'