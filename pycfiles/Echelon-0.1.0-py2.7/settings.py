# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/example_project/settings.py
# Compiled at: 2011-09-24 06:25:11
import os.path
ECHELON_ROOT = os.path.dirname(__import__('echelon').__file__)
DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'echelon.sqlite'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.admin', 'django.contrib.markup',
                  'devserver', 'echelon', 'south')
ADMIN_MEDIA_PREFIX = '/admin/media/'
ROOT_URLCONF = 'urls'
DEVSERVER_MODULES = ()
TEMPLATE_DIRS = (
 os.path.join(ECHELON_ROOT, 'templates', 'echelon'),)
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'echelon.context_processors.default',
                               'echelon.context_processors.root_categories', 'echelon.context_processors.settings')
try:
    from local_settings import *
except ImportError:
    pass