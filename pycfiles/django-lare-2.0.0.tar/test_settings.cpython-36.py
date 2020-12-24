# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonasbraun/Coding/iekadou/django-lare/django_lare/test_settings.py
# Compiled at: 2018-05-26 07:22:50
# Size of source mod 2**32: 5722 bytes
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = [
 '*']
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':'sqlite.db', 
             'USER':'', 
             'PASSWORD':'', 
             'HOST':'', 
             'PORT':''}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-uk'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
SECRET_KEY = 'u@x-aj9(hoh#rb-^ymf#g2jx_hp0vj7u5#b@ag1n^seu9e!%cy'
import django
if django.VERSION >= (1, 10):
    MIDDLEWARE = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                  'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                  'django.contrib.messages.middleware.MessageMiddleware')
else:
    MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                          'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                          'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'tests'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages')
STATIC_URL = '/static/'
PASSWORD_HASHERS = ('django.contrib.auth.hashers.SHA1PasswordHasher', 'django.contrib.auth.hashers.PBKDF2PasswordHasher',
                    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher', 'django.contrib.auth.hashers.BCryptPasswordHasher',
                    'django.contrib.auth.hashers.MD5PasswordHasher', 'django.contrib.auth.hashers.CryptPasswordHasher')
AUTH_USER_MODEL = 'auth.User'
if django.VERSION < (1, 3):
    INSTALLED_APPS += ('staticfiles', )
else:
    INSTALLED_APPS += ('django_lare', )
    if django.VERSION >= (1, 7):
        import django
        django.setup()
    if django.VERSION <= (1, 9):
        from django.template.base import add_to_builtins
        add_to_builtins('django_lare.templatetags.lare_extends')
        TEMPLATE_CONTEXT_PROCESSORS = ('django_lare.context_processors.lare_information', )
    else:
        TEMPLATES = [
         {'BACKEND':'django.template.backends.django.DjangoTemplates', 
          'DIRS':[
           'django_lare/templates'], 
          'OPTIONS':{'context_processors':[
            'django_lare.context_processors.lare_information'], 
           'builtins':[
            'django_lare.templatetags.lare_extends']}}]
    if django.VERSION >= (1, 10):
        MIDDLEWARE += ('django_lare.middlewares.LareMiddleware', )
        TEMPLATES = [
         {'BACKEND':'django.template.backends.django.DjangoTemplates', 
          'DIRS':[
           'django_lare/templates'], 
          'OPTIONS':{'context_processors':[
            'django_lare.context_processors.lare_information'], 
           'builtins':[
            'django_lare.templatetags.lare_extends'], 
           'loaders':[
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader']}}]
    else:
        TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
    MIDDLEWARE_CLASSES += ('django_lare.middlewares.LareMiddleware', )
DEFAULT_LARE_TEMPLATE = 'django_lare/lare.html'