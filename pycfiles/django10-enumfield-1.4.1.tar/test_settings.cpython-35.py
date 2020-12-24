# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jb/projects/i2biz/misc/django-enumfield/django_enumfield/tests/test_settings.py
# Compiled at: 2017-10-06 05:18:16
# Size of source mod 2**32: 418 bytes
import os
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': ':memory:'}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
INSTALLED_APPS = [
 'django_enumfield',
 'tests.models']
SECRET_KEY = 'iufoj=mibkpdz*%bob952x(%49rqgv8gg45k36kjcg76&-y5=!'