# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-country-dialcode/country_dialcode/tests/test_settings.py
# Compiled at: 2014-07-16 08:17:07
import os
from country_dialcode.compatibility import text_type
BASE_DIR = os.path.dirname(__file__)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.sessions', 'django.contrib.contenttypes',
                  'django.contrib.admin', 'country_dialcode')
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware')
ROOT_URLCONF = 'urls'
SECRET_KEY = 'secretkey'
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

class InvalidVarException(object):

    def __mod__(self, missing):
        try:
            missing_str = text_type(missing)
        except:
            missing_str = 'Failed to create string representation'

        raise Exception('Unknown template variable %r %s' % (missing, missing_str))

    def __contains__(self, search):
        if search == '%s':
            return True
        return False


TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = InvalidVarException()