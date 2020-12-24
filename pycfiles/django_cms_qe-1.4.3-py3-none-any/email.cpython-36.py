# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/email.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 357 bytes
"""
Mailing settings, by default app looks for smtp server.
"""
EMAIL_HOST = 'localhost'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = 'django_cms_qe@localhost'