# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/examples/_django/settings.py
# Compiled at: 2013-12-04 14:19:17
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.', 
               'NAME': '', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = '../../'
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'ey%7==a_#)hng+6l96$=bb*gwdf=@_%toqj0^pn1z@72tfi(_m'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', )
MIDDLEWARE_CLASSES = ()
ROOT_URLCONF = '_django.urls'
import os
TEMPLATE_DIRS = (
 os.path.abspath(os.path.dirname(__file__) + '/templates'),)
INSTALLED_APPS = ()
LOGGING = {'version': 1, 
   'disable_existing_loggers': True, 
   'formatters': {'simple': {'format': '%(levelname)s:%(asctime)s:%(message)s'}}, 
   'handlers': {'stdout': {'level': 'DEBUG', 
                           'class': 'logging.StreamHandler', 
                           'formatter': 'simple'}}, 
   'loggers': {'pyws': {'handlers': [
                                   'stdout'], 
                        'propagate': True, 
                        'level': 'DEBUG'}}}