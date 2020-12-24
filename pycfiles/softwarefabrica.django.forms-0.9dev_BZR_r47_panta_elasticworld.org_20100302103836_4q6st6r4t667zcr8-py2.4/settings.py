# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/forms/tests/settings.py
# Compiled at: 2008-12-22 09:11:43
import os
DIRNAME = os.path.dirname(__file__)
DEFAULT_CHARSET = 'utf-8'
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(DIRNAME, 'forms_test.db')
TEMPLATE_DEBUG = True
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
TEMPLATE_DIRS = (
 os.path.join(DIRNAME, 'templates'),)
INSTALLED_APPS = ('django.contrib.contenttypes', 'softwarefabrica.django.utils', 'softwarefabrica.django.forms',
                  'softwarefabrica.django.forms.tests')