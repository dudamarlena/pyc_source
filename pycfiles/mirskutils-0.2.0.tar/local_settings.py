# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./webapp/local_settings.py
# Compiled at: 2014-06-01 18:41:18
import os
gettext = lambda s: s
DEBUG = True
TEMPLATE_DEBUG = True
DEBUGGER = True
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'site_static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
SESSION_COOKIE_DOMAIN = 'starter-app.com'
COMPRESS_OUTPUT_DIR = 'CACHE'
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
ALLOWED_HOSTS = [
 '*']
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 
               'NAME': '', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
WINGHOME = '/Applications/WingIDE.app/Contents/MacOS/'
ACCOUNT_ACTIVATION_DAYS = 7
ADMINS = (('Super User', 'admin@domain.com'), )
MANAGERS = ADMINS
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'