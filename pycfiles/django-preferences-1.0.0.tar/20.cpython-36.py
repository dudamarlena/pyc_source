# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/tests/settings/20.py
# Compiled at: 2018-12-20 03:18:33
# Size of source mod 2**32: 1411 bytes
INSTALLED_APPS = ['django.contrib.auth',
 'django.contrib.sessions',
 'django.contrib.contenttypes',
 'django.contrib.admin',
 'django.contrib.sites',
 'preferences',
 'preferences.tests']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
MIDDLEWARE = ('django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware')
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[],  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.contrib.auth.context_processors.auth',
                          'django.template.context_processors.debug',
                          'django.template.context_processors.i18n',
                          'django.template.context_processors.media',
                          'django.template.context_processors.static',
                          'django.template.context_processors.tz',
                          'django.template.context_processors.request',
                          'django.contrib.messages.context_processors.messages',
                          'preferences.context_processors.preferences_cp']}}]
ROOT_URLCONF = 'preferences.tests.urls'
SECRET_KEY = 'test_secret_key'