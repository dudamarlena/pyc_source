# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/settings/django_settings.py
# Compiled at: 2014-06-27 19:07:27
import gettext
ALLOWED_HOSTS = ['localhost']
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
SECRET_KEY = ''
LANGUAGE_CODE = 'en-us'
ugettext = lambda s: s
LANGUAGES = (
 (
  'en', ugettext('American English')),)
TEMPLATE_DIRS = []
TEMPLATE_LOADERS = [
 'django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader']
MIDDLEWARE_CLASSES = [
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'debug_toolbar.middleware.DebugToolbarMiddleware']
TEMPLATE_CONTEXT_PROCESSORS = [
 'django.contrib.auth.context_processors.auth',
 'django.contrib.messages.context_processors.messages',
 'django.core.context_processors.debug',
 'django.core.context_processors.i18n',
 'django.core.context_processors.media',
 'django.core.context_processors.static',
 'django.core.context_processors.request',
 'django.core.context_processors.tz',
 'sekizai.context_processors.sekizai']
STATICFILES_FINDERS = [
 'django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 'compressor.finders.CompressorFinder']
AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend']