# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/django-blastplus/blastplus/test_settings.py
# Compiled at: 2018-05-23 09:38:26
# Size of source mod 2**32: 1689 bytes
from blastplus.settings import *
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':'abc'}}
INSTALLED_APPS = [
 'django.contrib.contenttypes',
 'django.contrib.staticfiles',
 'django.contrib.auth',
 'django_nose',
 'coverage',
 'blastplus']
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'blastplus.urls'
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[
   os.path.join(BASE_DIR, 'blastplus/templates')], 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.contrib.auth.context_processors.auth',
                          'django.template.context_processors.debug',
                          'django.template.context_processors.i18n',
                          'django.template.context_processors.media',
                          'django.template.context_processors.static',
                          'django.template.context_processors.tz',
                          'django.contrib.messages.context_processors.messages']}}]
STATIC_URL = '/static/'
SECRET_KEY = 'set-secret-key-here'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
 '--with-coverage',
 '--cover-package=blastplus',
 '--cover-inclusive',
 '--verbosity=2']