# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/configurable_settings.py
# Compiled at: 2014-08-28 04:16:05
import os, string, sys, dj_database_url, shortuuid
from signalbox.utilities.get_env_variable import get_env_variable
from twilio.rest import TwilioRestClient
DEBUG = bool(get_env_variable('DEBUG', required=False, default=False, as_yaml=True))
LOG_DATABASE_QUERIES = get_env_variable('LOG_DATABASE_QUERIES', required=False, default=False)
BRAND_NAME = get_env_variable('BRAND_NAME', default='SignalBox')
DEFAULT_TELEPHONE_COUNTRY_CODE = get_env_variable('DEFAULT_TELEPHONE_COUNTRY_CODE', default='GB')
LOGIN_FROM_OBSERVATION_TOKEN = get_env_variable('LOGIN_FROM_OBSERVATION_TOKEN', default=False)
SHOW_USER_CURRENT_STUDIES = get_env_variable('SHOW_USER_CURRENT_STUDIES', default=False)
DEFAULT_USER_PROFILE_FIELDS = get_env_variable('DEFAULT_USER_PROFILE_FIELDS', default='').split(',')
os.environ['REUSE_DB'] = '1'
DB_URL = get_env_variable('DATABASE_URL', required=False, default='postgres://localhost/sbox')
DATABASES = {'default': dj_database_url.config(default=DB_URL)}
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS', default='127.0.0.1;.herokuapp.com').split(';')
SESSION_COOKIE_HTTPONLY = get_env_variable('SESSION_COOKIE_HTTPONLY', default=True)
SECURE_BROWSER_XSS_FILTER = get_env_variable('SECURE_BROWSER_XSS_FILTER', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = get_env_variable('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_SSL_REDIRECT = get_env_variable('SECURE_SSL_REDIRECT', required=False, default=False)
SESSION_COOKIE_AGE = get_env_variable('SESSION_COOKIE_AGE', default=7200)
SESSION_SAVE_EVERY_REQUEST = get_env_variable('SESSION_SAVE_EVERY_REQUEST', default=True)
SESSION_EXPIRE_AT_BROWSER_CLOSE = get_env_variable('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=True)
SESSION_COOKIE_SECURE = get_env_variable('SESSION_COOKIE_SECURE', default=False)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_FRAME_DENY = False
USE_VERSIONING = get_env_variable('USE_VERSIONING', default=False)
TTS_VOICE = get_env_variable('TTS_VOICE', default='female')
TTS_LANGUAGE = get_env_variable('TTS_LANGUAGE', default='en-gb')
SECRET_KEY = get_env_variable('SECRET_KEY', default=shortuuid.uuid())
try:
    TESTING = 'test' == sys.argv[1]
except IndexError:
    TESTING = False

if bool('test' in sys.argv):
    print 'Turning on versioning because we are testing'
    USE_VERSIONING = True
ALLOWED_UPLOAD_MIME_TYPES = [
 'application/pdf',
 'image/png',
 'image/jpeg',
 'image/gif']
SHELL_PLUS_PRE_IMPORTS = (
 (
  'signalbox.models', ('*', )),
 ('ask.models', '*'),
 ('django.contrib.auth.models', 'User'))