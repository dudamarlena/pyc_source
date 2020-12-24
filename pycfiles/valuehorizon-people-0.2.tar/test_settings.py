# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quincy/Code/valuehorizon-people/people/settings/test_settings.py
# Compiled at: 2015-05-29 13:58:44
"""Settings that need to be set in order to run the tests."""
import os, logging
DEBUG = True
logging.getLogger('factory').setLevel(logging.WARN)
SITE_ID = 1
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': ':memory:'}}
ROOT_URLCONF = 'people.tests.urls'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../app_static')
MEDIA_ROOT = os.path.join(APP_ROOT, '../app_media')
STATICFILES_DIRS = (
 os.path.join(APP_ROOT, 'static'),)
TEMPLATE_DIRS = (
 os.path.join(APP_ROOT, 'tests/test_app/templates'),)
EXTERNAL_APPS = [
 'django.contrib.admin',
 'django.contrib.admindocs',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.messages',
 'django.contrib.sessions',
 'django.contrib.staticfiles',
 'django.contrib.sitemaps',
 'django.contrib.sites',
 'django_nose',
 'forex',
 'countries']
INTERNAL_APPS = [
 'people']
INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS
MIDDLEWARE_CLASSES = [
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware']
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(os.path.join(APP_ROOT, 'tests/coverage'))
COVERAGE_MODULE_EXCLUDES = [
 'tests$', 'settings$', 'urls$', 'locale$',
 'migrations', 'fixtures', 'admin$', 'django_extensions']
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS
SECRET_KEY = 'foobar'