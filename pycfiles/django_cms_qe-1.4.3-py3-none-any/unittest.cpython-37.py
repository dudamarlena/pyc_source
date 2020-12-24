# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/unittest.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 499 bytes
"""
Configuration for unit testing.
"""
from .dev import *
ROOT_URLCONF = 'cms_qe.urls'
ALDRYN_BOILERPLATE_NAME = 'legacy'
PASSWORD_HASHERS = [
 'django.contrib.auth.hashers.MD5PasswordHasher']
TEST_MAILCHIMP_USERNAME = 'cms-qe-test'
TEST_MAILCHIMP_API_KEY = '4b1f852f66a317a500a5ae711a9181be-us16'
TEST_MAILCHIMP_LIST_ID = 'b6b91697ec'