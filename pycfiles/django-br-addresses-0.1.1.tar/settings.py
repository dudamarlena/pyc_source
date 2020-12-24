# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucas/workspace-python/django-br-addresses/tests/settings.py
# Compiled at: 2014-11-14 20:38:40
SECRET_KEY = 'te$T1ng'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.contrib.redirects.middleware.RedirectFallbackMiddleware')
INSTALLED_APPS = [
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.sites',
 'django.contrib.admin',
 'django.contrib.redirects',
 'django_extensions',
 'localflavor',
 'django_br_addresses']
SITE_ID = 1
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_DISCOVER_PATTERN = 'test_*'
NOSE_ARGS = [
 '--verbosity=2',
 '-x',
 '-d',
 '--with-specplugin',
 '--with-xtraceback',
 '--with-progressive']