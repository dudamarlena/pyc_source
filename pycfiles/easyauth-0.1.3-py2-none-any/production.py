# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\mine\PycharmProjects\easyauth\test\settings\production.py
# Compiled at: 2018-12-26 23:55:28
"""Production settings."""
import os
from os.path import abspath, basename, dirname, join, normpath, isdir
from sys import path
APP_ROOT = dirname(dirname(abspath(__file__)))
APP_NAME = basename(APP_ROOT)
WK_DIR = dirname(APP_ROOT)
path.append(WK_DIR)
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': normpath(join(WK_DIR, 'db.sqlite3')), 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = normpath(join(WK_DIR, 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = normpath(join(WK_DIR, 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
 normpath(join(WK_DIR, 'vue-ui/dist')),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = 'a@m_u@22l@r0m)pgkm(unp2dll-14ms&aw%e-svhrdf$g657us'
FIXTURE_DIRS = (
 normpath(join(WK_DIR, 'fixtures')),)
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.core.context_processors.static', 'django.core.context_processors.tz',
                               'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.request')
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
TEMPLATE_DIRS = (
 normpath(join(WK_DIR, 'templates')),)
MIDDLEWARE_CLASSES = ('django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware',
                      'corsheaders.middleware.CorsMiddleware', 'easyauth.middleware.SwitchLanguageMiddleware',
                      'easyauth.middleware.RequestLoggingMiddleware')
DJANGO_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
               'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.admin')
LOCAL_APPS = (
 'rest_framework',
 'django_filters',
 'corsheaders',
 'easyauth',
 '%s' % APP_NAME)
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 
   'handlers': {'mail_admins': {'level': 'ERROR', 
                                'filters': [
                                          'require_debug_false'], 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': True}}}
WSGI_APPLICATION = '%s.wsgi.application' % APP_NAME
ROOT_URLCONF = '%s.urls' % APP_NAME
INSTALLED_APPS += ()
AUTH_PASSWORD_VALIDATORS = [
 {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
 {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
 {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
 {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ('easyauth.permissions.IsAuthenticated', ), 
   'DEFAULT_AUTHENTICATION_CLASSES': ('easyauth.authentication.CsrfExemptSessionAuthentication', 'rest_framework.authentication.BasicAuthentication'), 
   'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ), 
   'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser', 'rest_framework.parsers.MultiPartParser'), 
   'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter',
 'rest_framework.filters.OrderingFilter'), 
   'EXCEPTION_HANDLER': 'easyauth.views.exception_handler', 
   'DEFAULT_PAGINATION_CLASS': 'easyauth.pagination.CustomizedPageNumberPagination', 
   'PAGE_SIZE': 500}
AUTH_USER_MODEL = '%s.User' % APP_NAME
ALLOWED_HOSTS = [
 '*']
LOCALE_PATHS = ('/locale', )
LOG_ROOT_PATH = join(WK_DIR, 'logs')
if not isdir(LOG_ROOT_PATH):
    os.mkdir(LOG_ROOT_PATH)
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'filters': {'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}, 
               'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 
   'formatters': {'standard': {'format': '%(asctime)s %(levelname)s [%(threadName)s] [%(name)s] %(pathname)s %(funcName)s %(lineno)d: %(message)s'}, 
                  'simple': {'format': '%(asctime)s %(levelname)s [%(threadName)s] [%(name)s] %(message)s'}}, 
   'handlers': {'null': {'class': 'logging.NullHandler'}, 
                'server_log': {'level': 'DEBUG', 
                               'class': 'logging.handlers.RotatingFileHandler', 
                               'filename': os.path.join(LOG_ROOT_PATH, 'server.log'), 
                               'maxBytes': 5242880, 
                               'backupCount': 5, 
                               'encoding': 'UTF-8', 
                               'formatter': 'simple'}, 
                'console': {'level': 'DEBUG', 
                            'filters': [
                                      'require_debug_true'], 
                            'class': 'logging.StreamHandler', 
                            'formatter': 'simple'}}, 
   'loggers': {'django': {'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'), 
                          'propagate': True}, 
               'django.security.DisallowedHost': {'handlers': [
                                                             'null'], 
                                                  'propagate': False}, 
               'django.db.backends': {'level': os.getenv('DJANGO_DB_BACKEND_LOG_LEVEL', 'INFO'), 
                                      'propagate': True}, 
               'easyauth': {'level': os.getenv('EASYAUTH_LOG_LEVEL', 'INFO'), 
                            'propagate': True}, 
               '': {'handlers': [
                               'server_log', 'console'], 
                    'level': 'INFO', 
                    'propagate': True}}}
SESSION_COOKIE_AGE = 604800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
EASYAUTH_CONF = {'USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN': '12345678', 
   'ACCOUNT_LOGOUT_ON_GET': True, 
   'DISABLE_REGISTER': False, 
   'LANG_PARAM': 'lang'}