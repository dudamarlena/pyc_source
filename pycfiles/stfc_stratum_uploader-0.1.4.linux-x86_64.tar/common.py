# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/settings/common.py
# Compiled at: 2013-08-16 09:55:14
from configurations import Settings
import os

def get_host_name():
    import socket
    try:
        return socket.gethostname()
    except socket.error:
        return 'localhost'


class Common(Settings):
    ADMINS = (('root', 'email@example.com'), )
    MANAGERS = ADMINS
    PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '../../..'))
    HOSTNAME = get_host_name()
    TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.debug',
                                   'django.core.context_processors.i18n', 'django.core.context_processors.media',
                                   'django.core.context_processors.static', 'django.core.context_processors.tz',
                                   'django.contrib.messages.context_processors.messages')
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
                   'NAME': '%s/db/uploader_dev.sqlite3' % PROJECT_ROOT, 
                   'TEST_NAME': ':memory:', 
                   'USER': '', 
                   'PASSWORD': '', 
                   'HOST': '', 
                   'PORT': ''}}
    ALLOWED_HOSTS = []
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    SITE_ID = 1
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads/')
    MEDIA_URL = 'http://%s/uploads/' % HOSTNAME
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collectstatic/')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
     os.path.join(PROJECT_ROOT, 'archer/static/'),)
    STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
    SECRET_KEY = 'apksigo!uh4gth@7nco7y2biavj=0fxd0b3@2!ax6*rb29fq=w'
    TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
    MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                          'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                          'archer.core.middleware.CustomHeaderMiddleware', 'django.contrib.messages.middleware.MessageMiddleware')
    ROOT_URLCONF = 'archer.urls'
    WSGI_APPLICATION = 'archer.wsgi.application'
    TEMPLATE_DIRS = (
     os.path.join(os.path.dirname(__file__), '../../', 'templates').replace('\\', '/'),)
    INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                      'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.admin',
                      'archer.core', 'archer.custom_auth', 'archer.projects', 'archer.packages',
                      'archer.appsetup', 'django_extensions', 'bootstrap_toolkit',
                      'guardian', 'south')
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
    LOGIN_URL = 'unauthenticated'
    AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.RemoteUserBackend', 'django.contrib.auth.backends.ModelBackend',
                               'guardian.backends.ObjectPermissionBackend')
    AUTH_USER_MODEL = 'custom_auth.User'
    ANONYMOUS_USER_ID = 1
    FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures/')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'