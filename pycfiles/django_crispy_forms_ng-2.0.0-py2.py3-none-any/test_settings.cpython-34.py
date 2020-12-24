# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-crispy-forms/django-crispy-forms-ng/crispy_forms/tests/test_settings.py
# Compiled at: 2015-04-08 09:59:08
# Size of source mod 2**32: 1780 bytes
import os
from django.utils import six
BASE_DIR = os.path.dirname(__file__)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.sessions', 'django.contrib.contenttypes',
                  'django.contrib.admin', 'crispy_forms')
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware')
ROOT_URLCONF = 'urls'
CRISPY_CLASS_CONVERTERS = {'textinput': 'textinput textInput inputtext'}
SECRET_KEY = 'secretkey'
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

class InvalidVarException(object):

    def __mod__(self, missing):
        try:
            missing_str = six.text_type(missing)
        except:
            missing_str = 'Failed to create string representation'

        raise Exception('Unknown template variable %r %s' % (missing, missing_str))

    def __contains__(self, search):
        if search == '%s':
            return True
        return False


TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = InvalidVarException()
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
  'APP_DIRS': True, 
  'DIRS': [],  'OPTIONS': {'context_processors': [
                                     'django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages'], 
              'debug': True, 
              'string_if_invalid': InvalidVarException()}}]