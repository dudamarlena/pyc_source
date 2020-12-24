# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/forum/settings_travis.py
# Compiled at: 2013-07-02 04:51:32
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'dinette.db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = 'dinette/media/'
MEDIA_URL = '/site_media/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '9oezy17)u&_!3n%@qb^iqz%ur2%v(5=0uas@@#4)=n@5xy3m1j'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'pagination.middleware.PaginationMiddleware')
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = ()
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.request', 'django.core.context_processors.static')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.admin',
                  'django.contrib.staticfiles', 'dinette', 'compressor', 'google_analytics',
                  'sorl.thumbnail', 'openid_consumer', 'pagination')
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'dev.db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
from dinette.extra_settings import *
import os
from subprocess import call
from markupfield.markup import DEFAULT_MARKUP_TYPES
from dinette.libs.postmarkup import render_bbcode
COMPRESS = False
DEFAULT_MARKUP_TYPES.append(('bbcode', render_bbcode))
MARKUP_RENDERERS = DEFAULT_MARKUP_TYPES
DEFAULT_MARKUP_TYPE = 'bbcode'
logfilename = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logging.conf')
LOG_FILE_NAME = logfilename
LOG_FILE_PATH = '"' + os.path.join(os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logs'), 'logs.txt') + '"'
log_file_dir = '%s/forum/logs' % os.getcwd()
if not os.path.exists(log_file_dir):
    call(['mkdir', log_file_dir])
AUTH_PROFILE_MODULE = 'dinette.DinetteUserProfile'
REPLY_PAGE_SIZE = 10
FLOOD_TIME = 0
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'compressor.finders.CompressorFinder')
STATIC_URL = '/static/'