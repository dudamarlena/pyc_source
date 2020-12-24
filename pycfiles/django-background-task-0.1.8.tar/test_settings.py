# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tests/test_settings.py
# Compiled at: 2013-01-07 04:44:16
import sys
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ':memory:'
DATABASES = {'default': {'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE, 
               'NAME': DATABASE_NAME, 
               'USER': '', 
               'PASSWORD': ''}}
INSTALLED_APPS = [
 'background_task']
if 'test_coverage' in sys.argv:
    INSTALLED_APPS.append('django_coverage')
    COVERAGE_REPORT_HTML_OUTPUT_DIR = 'html_coverage'
    COVERAGE_MODULE_EXCLUDES = []