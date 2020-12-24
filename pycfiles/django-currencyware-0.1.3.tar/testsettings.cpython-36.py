# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-tisqp5jr/django-currencyware/currencyware/tests/testsettings.py
# Compiled at: 2018-08-22 09:57:42
# Size of source mod 2**32: 1385 bytes
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':':memory:'}}
SECRET_KEY = 'un33k'
STATICFILES_FINDERS = [
 'django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 'django.contrib.staticfiles.finders.DefaultStorageFinder']
TEMPLATE_LOADERS = [
 'django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader']
TEMPLATE_CONTEXT_PROCESSORS = [
 'django.contrib.auth.context_processors.auth',
 'django.core.context_processors.debug',
 'django.core.context_processors.request',
 'django.contrib.messages.context_processors.messages']
INSTALLED_APPS = [
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.sites',
 'django.contrib.humanize',
 'django.contrib.admin',
 'currencyware']
MIDDLEWARE_CLASSES = []
ROOT_URLCONF = 'currencyware.tests.urls'
SITE_ID = 1
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
PRIORITY_CURRENCY_CODES = [
 'CAD']