# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/forum/localsettings.py
# Compiled at: 2013-07-02 05:28:19
import os
TOPIC_PAGE_SIZE = 3
REPLY_PAGE_SIZE = 12
AUTH_PROFILE_MODULE = 'dinette.DinetteUserProfile'
RANKS_NAMES_DATA = ((30, 'Member'), (100, 'Senior Member'), (300, 'Star'))
DINETTE_LOGIN_TEMPLATE = 'dinette/social_login.html'
LOG_FILE_PATH = '"' + os.path.join(os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logs'), 'logs.txt') + '"'
LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logging.conf')
FLOOD_TIME = 1000
HAYSTACK_SITECONF = 'dinette.search'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'index.db')
SITE_URL = 'http://127.0.0.1:8000'
LOGIN_REDIRECT_URL = '/forum/'
LOGOUT_REDIRECT_URL = '/forum/'
LOGIN_URL = '/accounts/login/'
OPENID_REDIRECT_NEXT = '/accounts/openid/done/'
OPENID_SREG = {'requred': 'nickname, email, fullname', 'optional': 'postcode, country', 
   'policy_url': ''}
OPENID_AX = [
 {'type_uri': 'http://axschema.org/contact/email', 'count': 1, 
    'required': True, 
    'alias': 'email'},
 {'type_uri': 'http://axschema.org/schema/fullname', 'count': 1, 
    'required': False, 
    'alias': 'fname'}]
OPENID_AX_PROVIDER_MAP = {'Google': {'email': 'http://axschema.org/contact/email', 'firstname': 'http://axschema.org/namePerson/first', 
              'lastname': 'http://axschema.org/namePerson/last'}, 
   'Default': {'email': 'http://axschema.org/contact/email', 'fullname': 'http://axschema.org/namePerson', 
               'nickname': 'http://axschema.org/namePerson/friendly'}}
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'socialauth.auth_backends.OpenIdBackend',
                           'socialauth.auth_backends.TwitterBackend', 'socialauth.auth_backends.FacebookBackend',
                           'socialauth.auth_backends.LinkedInBackend')
from markupfield.markup import DEFAULT_MARKUP_TYPES
MARKUP_RENDERERS = DEFAULT_MARKUP_TYPES
DEFAULT_MARKUP_TYPE = 'plain'