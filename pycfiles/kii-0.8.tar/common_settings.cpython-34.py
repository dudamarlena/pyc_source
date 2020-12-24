# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/glue/common_settings.py
# Compiled at: 2015-01-18 13:17:01
# Size of source mod 2**32: 3504 bytes
"""Base settings shared by all environments"""
from django.conf.global_settings import *
from django.core.urlresolvers import reverse_lazy
import os, kii
KII_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request', 'kii.app.context_processors.user_apps',
                                'kii.stream.context_processors.streams', 'kii.stream.context_processors.stream_models',
                                'kii.glue.context_processors.kii_metadata', 'kii.glue.context_processors.tracking_code',
                                'kii.activity.context_processors.unread_notifications')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.staticfiles', 'django.contrib.sites',
                  'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.admin',
                  'guardian', 'polymorphic', 'django_filters', 'mptt', 'rest_framework',
                  'autocomplete_light') + kii.APPS_CONFIGS + ('actstream', )
KII_APPS = kii.APPS
ALL_USERS_GROUP = 'all_users'
LOCALE_PATHS += (
 os.path.join(KII_DIR, 'locale'),)
SITE_ID = 1
STATIC_URL = '/static/'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
ANONYMOUS_USER_ID = -1
AUTHENTICATION_BACKENDS += ('guardian.backends.ObjectPermissionBackend', )
LOGIN_URL = 'kii:user:login'
REVERSED_LOGIN_URL = reverse_lazy(LOGIN_URL)
LOGIN_REDIRECT_URL = '/'
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (('en', 'English'), )
from django.utils.functional import curry
import markdown
from markdown.extensions.codehilite import makeExtension as CodeHilite
from kii.markdown.inlinepatterns import makeExtension as KiiFlavoredMarkdown
MARKDOWN_EXTENSIONS = (
 CodeHilite(css_class='code', linenums=False, noclasses=True),
 KiiFlavoredMarkdown())
md_filter = curry(markdown.markdown, extensions=MARKDOWN_EXTENSIONS)
MARKDOWN_FUNCTION = md_filter
MARKUP_FIELD_TYPES = (
 (
  'markdown', md_filter),
 (
  'none', lambda s: s))
TRACKING_CODE = ''
import logging
KII_LOGGER = logging.getLogger('kii')
LOGGING = {'version': 1, 
 'disable_existing_loggers': False, 
 'handlers': {'console': {'level': 'DEBUG', 
                          'class': 'logging.StreamHandler'}}, 
 'loggers': {'kii': {'handlers': [
                                  'console'], 
                     'level': 'DEBUG'}}}