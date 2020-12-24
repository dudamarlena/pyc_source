# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\django_microsip_base\settings\dev_plus.py
# Compiled at: 2019-09-30 12:05:46
from common import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
MODO_SERVIDOR = 'PRUEBAS'
MICROSIP_VERSION = '2017'
EXTRA_MODULES = ()
DJANGO_APPS += ('django_extensions', 'werkzeug_debugger_runserver')
from .common import get_microsip_extra_apps
MICROSIP_EXTRA_APPS, EXTRA_APPS = get_microsip_extra_apps(EXTRA_MODULES, is_dev=True)
INSTALLED_APPS = DJANGO_APPS + MICROSIP_MODULES + MICROSIP_EXTRA_APPS
ROOT_URLCONF = 'django_microsip_base.urls.dev'
STATICFILES_DIRS = (
 BASE_DIR + '/static/',)