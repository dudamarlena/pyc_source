# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/raton/pycharm_projects/django-hautomation-suite/django_hautomation_suite/django_hautomation_suite/settings.py
# Compiled at: 2014-06-30 03:45:01
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
HA_SERVER = 'HA_REST_API_HOST'
HA_PASSWORD = 'HA_REST_API_PASSWORD'
HA_USERNAME = 'HA_REST_API_USERNAME'
DJANGO_HAUTOMATION_DEPLOYED = False
DJANGO_HAWEB_DEPLOYED = False
DJANGO_THERMOMETER_DEPLOYED = False
DJANGO_THERMOSTAT_DEPLOYED = False
DATABASES = {'default': {'ENGINE': 'django.db.backends.', 
               'NAME': 'HA_DB_NAME', 
               'USER': 'HA_DB_USER', 
               'PASSWORD': 'HA_DB_PASSWORD', 
               'HOST': 'HA_DB_HOST', 
               'PORT': 'HA_DB_PORT'}}
ALLOWED_HOSTS = [
 'HA_WEB_SERVER_NAME']
TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = '/home/raton/komodo_work/pfg/whole/package/django-hautomation-suite/django_hautomation_suite/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = 'cr!vx#to^+*^y8*_0)_c25*4p(ksxb1=uwo*-zch+um(7d)631'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'django_hautomation_suite.urls'
WSGI_APPLICATION = 'django_hautomation_suite.wsgi.application'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'ha_cfg', 'hacore', 'harest', 'haweb', 'compressor', 'django_thermometer',
                  'django_thermostat', 'django.contrib.admin', 'gunicorn')
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