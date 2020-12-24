# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/settings.py
# Compiled at: 2018-11-13 04:54:27
# Size of source mod 2**32: 1023 bytes
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '//CrypyAPI_TEST_KEY//'
DEBUG = True
INSTALLED_APPS = [
 'cryptapi',
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.sites',
 'django.contrib.contenttypes',
 'django.contrib.sessions']
MIDDLEWARE = [
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'cryptapi.urls'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':'cryptapi.sqlite3'}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True