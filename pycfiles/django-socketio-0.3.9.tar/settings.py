# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steve/dev/django-socketio/django_socketio/example_project/settings.py
# Compiled at: 2013-11-04 16:45:11
import os, sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
full_path = lambda *parts: os.path.join(PROJECT_ROOT, *parts)
example_path = full_path('..', '..')
if example_path not in sys.path:
    sys.path.append(example_path)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'dev.db'}}
SECRET_KEY = 'i_!&$f5@^%y*i_qa$*o&0$3q*1dcv^@_-l2po8-%_$_gwo+i-l'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
STATIC_URL = '/static/'
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = full_path('templates')
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.staticfiles', 'django_socketio',
                  'chat')