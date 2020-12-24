# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/project/settings.py
# Compiled at: 2015-09-02 09:05:45
import os, sys
from os import path
FOUNDRY = {'sms_gateway_api_key': '', 
   'sms_gateway_password': ''}
LAYERS = {'layers': ('basic', )}
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)


PROJECT_MODULE = 'skeleton'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'skeleton.db', 
               'USER': 'skeleton', 
               'PASSWORD': 'skeleton', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = abspath('skeleton-media')
MEDIA_URL = '/media/'
STATIC_ROOT = abspath('static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
SECRET_KEY = 'SECRET_KEY_PLACEHOLDER'
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'foundry.middleware.CheckProfileCompleteness', 'django.contrib.messages.middleware.MessageMiddleware',
                      'likes.middleware.SecretBallotUserIpUseragentMiddleware', 'foundry.middleware.PaginationMiddleware',
                      'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.debug', 'django.core.context_processors.i18n',
                               'django.core.context_processors.media', 'django.core.context_processors.static',
                               'django.core.context_processors.request', 'preferences.context_processors.preferences_cp',
                               'foundry.context_processors.foundry')
TEMPLATE_LOADERS = ('layers.loaders.filesystem.Loader', 'django.template.loaders.filesystem.Loader',
                    'layers.loaders.app_directories.Loader', 'django.template.loaders.app_directories.Loader')
ROOT_URLCONF = 'project.urls'
INSTALLED_APPS = ('skeleton', 'foundry', 'contact', 'post', 'jmbo_analytics', 'jmbo',
                  'category', 'likes', 'photologue', 'secretballot', 'captcha', 'ckeditor',
                  'compressor', 'dfp', 'export', 'generate', 'googlesearch', 'gunicorn',
                  'object_tools', 'pagination', 'publisher', 'preferences', 'simple_autocomplete',
                  'sites_groups', 'snippetscream', 'social_auth', 'south', 'tastypie',
                  'django.contrib.auth', 'django.contrib.comments', 'django.contrib.contenttypes',
                  'django.contrib.flatpages', 'django.contrib.humanize', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.staticfiles', 'django.contrib.sitemaps',
                  'django.contrib.admin', 'djcelery', 'layers', 'raven.contrib.django',
                  'raven.contrib.django.celery')
RECAPTCHA_PUBLIC_KEY = '6LccPr4SAAAAAJRDO8gKDYw2QodyRiRLdqBhrs0n'
RECAPTCHA_PRIVATE_KEY = '6LccPr4SAAAAAH5q006QCoql-RRrRs1TFCpoaOcw'
ROOT_GIZMOCONF = '%s.gizmos' % PROJECT_MODULE
CKEDITOR_MEDIA_PREFIX = '/media/ckeditor/'
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
CKEDITOR_CONFIGS = {'default': {'toolbar_Full': [
                              [
                               'Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
                              [
                               'Link', 'Image', 'Flash', 'PageBreak'],
                              [
                               'TextColor', 'BGColor'],
                              [
                               'Smiley', 'SpecialChar'], ['Source']]}}
CKEDITOR_RESTRICT_BY_USER = True
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = ('foundry.backends.MultiBackend', 'django.contrib.auth.backends.ModelBackend',
                           'social_auth.backends.facebook.FacebookBackend', 'social_auth.backends.twitter.TwitterBackend')
COMMENTS_APP = 'foundry'
SIMPLE_AUTOCOMPLETE = {'auth.user': {'threshold': 20, 'search_field': 'username'}, 'category.category': {'threshold': 20}, 'jmbo.modelbase': {'threshold': 50, 
                      'duplicate_format_function': lambda item, model, content_type: item.as_leaf_class().content_type.name}}
STATICFILES_FINDERS = ('layers.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.FileSystemFinder',
                       'layers.finders.AppDirectoriesFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'compressor.finders.CompressorFinder')
ADMIN_APPS_EXCLUDE = ('Cal', 'Event', 'Photologue', 'Publisher', 'Registration', 'Auth')
ADMIN_MODELS_EXCLUDE = ('Groups', 'Video files')
JMBO_ANALYTICS = {'google_analytics_id': 'xxx'}
PHOTOLOGUE_MAXBLOCK = 1048576
DJANGO_ATLAS = {'google_maps_api_key': 'AIzaSyBvdwGsAn2h6tNI75M5cAcryln7rrTYqkk'}
LOGGING = {'version': 1, 
   'disable_existing_loggers': True, 
   'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 
   'formatters': {'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'}}, 
   'handlers': {'console': {'level': 'WARN', 
                            'class': 'logging.StreamHandler', 
                            'formatter': 'verbose'}, 
                'sentry': {'level': 'ERROR', 
                           'filters': [
                                     'require_debug_false'], 
                           'class': 'raven.contrib.django.handlers.SentryHandler'}}, 
   'loggers': {'raven': {'level': 'ERROR', 
                         'handlers': [
                                    'console'], 
                         'propagate': True}, 
               'sentry.errors': {'level': 'ERROR', 
                                 'handlers': [
                                            'console'], 
                                 'propagate': True}, 
               'django': {'handlers': [
                                     'console'], 
                          'level': 'WARN', 
                          'propagate': False}}}
SOCIAL_AUTH_USER_MODEL = 'foundry.Member'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
COMPRESS_CSS_HASHING_METHOD = 'content'
CELERY_QUEUES = {'default': {'exchange': 'celery', 
               'binding_key': 'celery'}, 
   'sentry': {'exchange': 'celery', 
              'binding_key': 'sentry'}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
import djcelery
djcelery.setup_loader()