# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gmsdk/__init__.py
# Compiled at: 2015-04-06 14:46:48
import re
from django.conf import settings
from gmsdk.utils import get_auth_token, _input_credentials
from gmsdk.app_settings import CONFIG
from django.core.exceptions import ImproperlyConfigured
token = ''

def validate_settings():
    """
    Description:
        Validator for validating settings
    """
    if HOST not in CONFIG['host']:
        raise AttributeError
    if not AUTH_TOKEN:
        token_input = raw_input("Token Not Found. Press 'y' to login and generate token.\n")
        if token_input == 'y':
            token = _input_credentials(HOST)
            print 'Enter the token generated in settings GODAM_AUTH_TOKEN = %s and try again.' % token
            exit()
        else:
            raise AttributeError


try:
    AUTH_TOKEN = getattr(settings, 'GODAM_AUTH_TOKEN')
    HOST = getattr(settings, 'GODAM_HOST')
    validate_settings()
except AttributeError as e:
    print '\nApp gmsdk is not configured properly. Try Again.'
    print "Enter the following appropriate details in the settings file to continue :\n GODAM_HOST_TOKEN =  ('godam.delhivery.com' Prod Envitonment or 'stg-godam.delhivery.com' Test Environment)\n GODAM_AUTH_TOKEN =  (Enter token)"
    exit()

from gmsdk.api import GMSDK