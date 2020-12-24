# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/settings/test.py
# Compiled at: 2015-08-31 13:52:46
"""
Test-specific Django settings.
"""
from .base import *
TEST_APPS = ('ubcpi', )
NOSE_ARGS = [
 '-a !acceptance',
 '--with-coverage',
 '--cover-package=' + (',').join(TEST_APPS),
 '--cover-branches',
 '--cover-erase']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'test_ubcpi', 
               'TEST_NAME': 'test_ubcpi'}, 
   'read_replica': {'ENGINE': 'django.db.backends.sqlite3', 
                    'TEST_MIRROR': 'default'}}
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
INSTALLED_APPS += ('django_nose', )
MEDIA_ROOT = os.path.join(BASE_DIR, 'storage/test')
import warnings
from django.core.cache import CacheKeyWarning
warnings.simplefilter('ignore', CacheKeyWarning)