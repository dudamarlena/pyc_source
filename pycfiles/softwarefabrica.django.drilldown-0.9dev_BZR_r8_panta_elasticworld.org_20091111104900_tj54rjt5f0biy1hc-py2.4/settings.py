# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/drilldown/tests/settings.py
# Compiled at: 2009-11-11 02:57:50
import os
DIRNAME = os.path.dirname(__file__)
DEFAULT_CHARSET = 'utf-8'
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(DIRNAME, 'drilldown_test.db')
TEMPLATE_DEBUG = True
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
TEMPLATE_DIRS = (
 os.path.join(DIRNAME, 'templates'),)
SITE_ID = 1
TEST_RUNNER = 'softwarefabrica.django.utils.runners.run_tests'
TEST_APPS = ('tests', )
COVERAGE_MODULES = ('softwarefabrica.django.drilldown.models', )
import logging
if not hasattr(logging, 'VERBOSE'):
    logging.VERBOSE = 15
    logging._levelNames['VERBOSE'] = logging.VERBOSE
    logging._levelNames[logging.VERBOSE] = 'VERBOSE'
logging.basicConfig(level=logging.DEBUG)
ROOT_URLCONF = 'softwarefabrica.django.drilldown.tests.urls'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.admin', 'django.contrib.markup',
                  'softwarefabrica.django.utils', 'softwarefabrica.django.forms',
                  'softwarefabrica.django.crud', 'softwarefabrica.django.common',
                  'softwarefabrica.django.drilldown', 'softwarefabrica.django.drilldown.tests')