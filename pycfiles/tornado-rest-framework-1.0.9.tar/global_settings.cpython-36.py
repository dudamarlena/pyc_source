# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/conf/global_settings.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 2395 bytes
DEBUG = False
TIME_ZONE = 'UTC'
SHOW_TIME_ZONE = 'UTC'
XSRF_COOKIES = False
CACHES = {'default': {'BACKEND':'rest_framework.core.cache.backend.simple', 
             'LOCATION':'', 
             'KEY_PREFIX':'', 
             'DEFAULT_TIMEOUT':300, 
             'OPTIONS':{'THRESHOLD': 500}}}
LANGUAGE_CODE = 'en_US'
LANGUAGE_DOMAIN = 'messages'
LANGUAGE_PATHS = []
DATABASES = {}
INSTALLED_APPS = []
PASSWORD_HASHERS = [
 'rest_framework.core.safe.hashers.PBKDF2PasswordHasher',
 'rest_framework.core.safe.hashers.PBKDF2SHA1PasswordHasher',
 'rest_framework.core.safe.hashers.Argon2PasswordHasher',
 'rest_framework.core.safe.hashers.BCryptSHA256PasswordHasher',
 'rest_framework.core.safe.hashers.BCryptPasswordHasher']
NON_FIELD_ERRORS = '__all__'
SEARCH_PARAM = 'search'
ORDERING_PARAM = 'order_field'
DATE_INPUT_FORMATS = [
 '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',
 '%b %d %Y', '%b %d, %Y',
 '%d %b %Y', '%d %b, %Y',
 '%B %d %Y', '%B %d, %Y',
 '%d %B %Y', '%d %B, %Y']
TIME_INPUT_FORMATS = [
 '%H:%M:%S',
 '%H:%M:%S.%f',
 '%H:%M']
DATETIME_INPUT_FORMATS = [
 '%Y-%m-%d %H:%M:%S',
 '%Y-%m-%d %H:%M:%S.%f',
 '%Y-%m-%d %H:%M',
 '%Y-%m-%d',
 '%m/%d/%Y %H:%M:%S',
 '%m/%d/%Y %H:%M:%S.%f',
 '%m/%d/%Y %H:%M',
 '%m/%d/%Y',
 '%m/%d/%y %H:%M:%S',
 '%m/%d/%y %H:%M:%S.%f',
 '%m/%d/%y %H:%M',
 '%m/%d/%y']
LOGGING = {}