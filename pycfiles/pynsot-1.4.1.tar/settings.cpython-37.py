# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/settings.py
# Compiled at: 2019-10-16 23:55:35
# Size of source mod 2**32: 13124 bytes
"""
Django settings for nsot project using Django 1.8.
"""
import macaddress
from netaddr import eui
import os, re, sys
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
CONF_ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = False
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django_extensions', 'django_filters', 'guardian', 'rest_framework',
                  'rest_framework_swagger', 'custom_user')
ANONYMOUS_USER_NAME = 'anonymous@service.local'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware',
                      'django.middleware.security.SecurityMiddleware')
APPEND_SLASH = True
TEMPLATES = [
 {'BACKEND':'django_jinja.backend.Jinja2', 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors':[
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.csrf',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages'], 
   'extensions':[
    'jinja2.ext.do',
    'jinja2.ext.loopcontrols',
    'jinja2.ext.with_',
    'jinja2.ext.i18n',
    'jinja2.ext.autoescape',
    'django_jinja.builtins.extensions.CsrfExtension',
    'django_jinja.builtins.extensions.CacheExtension',
    'django_jinja.builtins.extensions.TimezoneExtension',
    'django_jinja.builtins.extensions.UrlsExtension',
    'django_jinja.builtins.extensions.StaticFilesExtension',
    'django_jinja.builtins.extensions.DjangoFiltersExtension']}},
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[
   os.path.join(BASE_DIR, 'templates').replace('\\', '/')], 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.template.context_processors.csrf',
                          'django.template.context_processors.debug',
                          'django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth',
                          'django.contrib.messages.context_processors.messages']}}]
REST_FRAMEWORK = {'DEFAULT_FILTER_BACKENDS':('django_filters.rest_framework.DjangoFilterBackend', ), 
 'DEFAULT_RENDERER_CLASSES':[
  'rest_framework.renderers.JSONRenderer'], 
 'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination', 
 'DEFAULT_VERSIONING_CLASS':'rest_framework.versioning.AcceptHeaderVersioning', 
 'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.DjangoModelPermissions', ), 
 'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework.authentication.BasicAuthentication', 'rest_framework.authentication.SessionAuthentication'), 
 'TEST_REQUEST_DEFAULT_FORMAT':'json', 
 'PAGE_SIZE':None}
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':os.path.join(BASE_DIR, 'nsot.sqlite3')}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
SERVE_STATIC_FILES = True
USER_AUTH_HEADER = 'X-NSoT-Email'
AUTH_TOKEN_EXPIRY = 600
ALLOWED_HOSTS = [
 '*']
CSRF_COOKIE_NAME = '_xsrf'
SILENCED_SYSTEM_CHECKS = [
 'guardian.W001']
ANONYMOUS_USER_NAME = 'anonymous@service.local'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
 os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.realpath(os.path.join(BASE_DIR, 'staticfiles'))
SWAGGER_SETTINGS = {'exclude_namespaces': ['index']}
LOGGING = {'version':1, 
 'disable_existing_loggers':False, 
 'formatters':{'verbose':{'format':'[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s', 
   'datefmt':'%Y-%m-%d %H:%M:%S %z'}, 
  'simple':{'format': '%(levelname)s %(message)s'}}, 
 'handlers':{'console': {'level':'DEBUG', 
              'class':'logging.StreamHandler', 
              'stream':sys.stdout, 
              'formatter':'verbose'}}, 
 'loggers':{'django.request':{'handlers':[
    'console'], 
   'propagate':True, 
   'level':'ERROR'}, 
  'rest_framework':{'handlers':[
    'console'], 
   'level':'ERROR'}}}
ATTRIBUTE_NAME = re.compile('^[a-z][a-z0-9_]*$')
DEVICE_NAME = re.compile('^([A-Za-z0-9][A-Za-z0-9\\-]{0,61}[A-Za-z0-9]|[A-Za-z0-9])$')
MACADDRESS_DEFAULT_DIALECT = 'macaddress.mac_linux'
INTERFACE_DEFAULT_SPEED = 1000
INTERFACE_TYPE_CHOICES = ((6, 'ethernet'), (1, 'other'), (135, 'l2vlan'), (136, 'l3vlan'),
                          (161, 'lag'), (24, 'loopback'), (150, 'mpls'), (53, 'prop_virtual'),
                          (131, 'tunnel'))
INTERFACE_DEFAULT_TYPE = 6
NETWORK_INTERCONNECT_PREFIXES = (31, 127)
HOST_PREFIXES = (32, 128)
IP_VERSIONS = ('4', '6')