# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/settings.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 2051 bytes
__doc__ = '\nDjango settings for pf2 project.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/1.6/topics/settings/\n\nFor the full list of settings and their values, see\nhttps://docs.djangoproject.com/en/1.6/ref/settings/\n'
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '_vm(kzpbf(rd*54yec!48e19201*^)06e)+ipz3_89k(8ult5b'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'south', 'workgroups', 'projects', 'files')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'pf2.urls'
WSGI_APPLICATION = 'pf2.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 
             'NAME': 'printflow2', 
             'USER': 'colin', 
             'PASSWORD': 'paddy'}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'