# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wo0dyn/Projects/DjangoPimpMyTheme/example/example/settings.py
# Compiled at: 2017-06-08 05:05:12
"""
Django settings for example project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))
SECRET_KEY = '#^qtdm4ad9_44k+pf+2^ecrm(w9j@w(+s(^e$@s8l=zq%pqtwl'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.sites', 'pimpmytheme', 'example', 'subapp', 'compressor',
                  'django_nose')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'example', 'static')
STATIC_URL = '/static/'
SITE_ID = 1
COMPRESS_PRECOMPILERS = (('text/less', 'lessc {infile} {outfile}'), )
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'OPTIONS': {'context_processors': [
                                     'django.contrib.auth.context_processors.auth',
                                     'django.template.context_processors.request',
                                     'django.template.context_processors.static',
                                     'pimpmytheme.context_processors.get_site'], 
                'builtins': [
                           'django.templatetags.i18n',
                           'django.templatetags.static',
                           'django.templatetags.tz'], 
                'loaders': [
                          'pimpmytheme.template_loader.Loader',
                          'django.template.loaders.app_directories.Loader']}}]
STATICFILES_FINDERS = ('pimpmytheme.static_finder.CustomFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'compressor.finders.CompressorFinder')
NOSE_ARGS = [
 '--with-coverage',
 '--cover-package=pimpmytheme',
 '--verbosity=3',
 '--nocapture']
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CUSTOM_THEME_LOOKUP_OBJECT = 'example.models.PimpSite'
CUSTOM_THEME_LOOKUP_ATTR = 'name'
PIMPMYTHEME_FOLDER = os.path.join(BASE_DIR, 'pimp_theme')
LOGGING = {'version': 1, 
   'formatters': {'oneline': {'format': '%(asctime)s %(levelname)-8s %(name)s  %(message)s'}}, 
   'handlers': {'console': {'class': 'logging.StreamHandler', 
                            'formatter': 'oneline'}}, 
   'root': {'level': 'DEBUG', 
            'handlers': [
                       'console']}}