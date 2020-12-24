# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data1/home/davidm/egauge/django-epic-sample/epic-sample/epic-sample/settings.py
# Compiled at: 2016-11-07 23:52:50
# Size of source mod 2**32: 3798 bytes
"""
Django settings for epic-sample project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = ')rg1j00sq*po(cfq^868ptyj(sb9jo3m!ac5z0p21x)&%ccb&q'
DEBUG = True
ALLOWED_HOSTS = []
django_dir = os.path.dirname(__file__)
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
  'DIRS': [
           os.path.join(django_dir, 'templates')], 
  
  'APP_DIRS': True, 
  'OPTIONS': {'context_processors': [
                                     'django.contrib.auth.context_processors.auth']}}]
STATICFILES_DIRS = (
 os.path.join(django_dir, 'static'),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.humanize', 'dal', 'dal_select2', 'crispy_forms',
                  'bootstrap3_datetime', 'epic')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'epic-sample.urls'
WSGI_APPLICATION = 'epic-sample.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'
MEDIA_URL = '/media/'
EPIC_BILL_TO_ADDRESS = 'MyCompany Inc.\n1234 Street Blvd.\nSpaceport City, NM 87654'
EPIC_SHIPPING_TYPE = 'FedEx Ground'
EPIC_SHIPPING_ACCOUNT = '123456789'
EPIC_MANUFACTURER = 'MyCompany'
EPIC_KICAD_FOOTPRINTS_DIR = '/usr/local/lib/kicad-lib/footprints/'