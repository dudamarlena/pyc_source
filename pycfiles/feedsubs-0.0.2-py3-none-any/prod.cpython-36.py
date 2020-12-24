# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/feedsubs/settings/prod.py
# Compiled at: 2018-12-06 15:58:39
# Size of source mod 2**32: 3009 bytes
import pkg_resources
from .base import *
INSTALLED_APPS += [
 'raven.contrib.django',
 'ddtrace.contrib.django',
 'waitressd.apps.WaitressdConfig']
MIDDLEWARE = [
 'xff.middleware.XForwardedForMiddleware'] + ['waitressd.middleware.access_log'] + ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE + [
 'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware']
STATIC_ROOT = '/opt/static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
ALLOWED_HOSTS = [
 config('ALLOWED_HOST', default='feedsubs.com')]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https')
XFF_TRUSTED_PROXY_DEPTH = 1
DEFAULT_HTTP_PROTOCOL = 'https'
ADMINS = [
 ('Nicolas', 'nicolas@lemanchet.fr')]
MANAGERS = [('Nicolas', 'nicolas@lemanchet.fr')]
DEFAULT_FROM_EMAIL = 'hello@feedsubs.com'
EMAIL_BACKEND = 'spinach.contrib.spinachd.mail.BackgroundEmailBackend'
SERVER_EMAIL = 'hello@feedsubs.com'
EMAIL_HOST = 'smtp.eu.mailgun.org'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'hello@feedsubs.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 120
RAVEN_CONFIG = {'dsn':config('SENTRY_DSN'), 
 'release':pkg_resources.require('feedsubs')[0].version}
CACHES = {'default': {'TIMEOUT':86400, 
             'BACKEND':'django_redis.cache.RedisCache', 
             'LOCATION':config('REDIS_CACHE_URL', default='redis://'), 
             'OPTIONS':{'CLIENT_CLASS':'django_redis.client.DefaultClient', 
              'SOCKET_CONNECT_TIMEOUT':5, 
              'SOCKET_TIMEOUT':5, 
              'IGNORE_EXCEPTIONS':True}}}
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
WAITRESS = {'port':config('WAITRESS_PORT', default=8000, cast=int), 
 'asyncore_use_poll':True, 
 'threads':config('WAITRESS_THREADS', default=16, cast=int)}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'ams3'
AWS_S3_ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'feedsubs'
AWS_DEFAULT_ACL = 'private'
AWS_QUERYSTRING_EXPIRE = 7800
DATADOG_TRACE = {'DEFAULT_SERVICE':'feedsubs', 
 'INSTRUMENT_CACHE':False, 
 'TAGS':{'env': 'prod'}, 
 'AGENT_HOSTNAME':config('DD_AGENT_HOSTNAME', default='localhost'), 
 'AGENT_PORT':config('DD_AGENT_PORT', 8126, cast=int)}