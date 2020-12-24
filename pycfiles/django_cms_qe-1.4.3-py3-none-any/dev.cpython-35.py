# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/dev.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1292 bytes
"""
Configuration for development.

Disables all security options.
"""
import os
from typing import List
from .base import *
DEBUG = True
META_SITE_PROTOCOL = 'http'
SECRET_KEY = '^xzhq0*q1+t0*ihq^^1wuyj3i%y#(38b7d-vlpkm-d(=!^uk6x'
SESSION_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
ALLOWED_HOSTS = [
 'localhost']
INSTALLED_APPS += [
 'debug_toolbar',
 'django_extensions']
MIDDLEWARE += [
 'debug_toolbar.middleware.DebugToolbarMiddleware']
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'), 
             'TEST': {'NAME': ':memory:'}}}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'