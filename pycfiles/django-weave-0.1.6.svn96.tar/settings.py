# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jens/workspace/django-weave/trunk/testproject/settings.py
# Compiled at: 2010-04-07 04:49:12
"""
    testproject.settings
    ~~~~~~~~~~~~~~~~~~~~~~

    IMPORTANT:
        You should not edit this file!
        Owerwrite settings with a local settings file:
            local_settings.py

    Here are not all settings predifined you can use. Please look at the
    django documentation for a full list of all items:
        http://www.djangoproject.com/documentation/settings/

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author: JensDiemer $

    :copyleft: 2010 by the django-weave team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
import os, sys
try:
    import django, weave
except Exception, e:
    import traceback
    print '-' * 79
    sys.stderr.write(traceback.format_exc())
    print '-' * 79
    raise

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_ROOT, 'test.db3')
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = "Make this unique, and don't share it with anybody!"
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.csrf.middleware.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.middleware.transaction.TransactionMiddleware')
LOGIN_URL = 'admin'
ROOT_URLCONF = 'testproject.urls'
TEMPLATE_DIRS = (
 os.path.join(os.path.abspath(os.path.dirname(django.__file__)), 'contrib/admin/templates'),
 os.path.join(PROJECT_ROOT, 'templates'))
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.admin', 'django.contrib.admindocs',
                  'weave')
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''