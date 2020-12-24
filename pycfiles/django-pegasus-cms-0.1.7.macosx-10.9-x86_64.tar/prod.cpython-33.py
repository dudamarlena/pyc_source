# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/settings/prod.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 2743 bytes
from __future__ import absolute_import, division
from .base import *
DEBUG = False
TEMPLATE_DEBUG = False
SITE_ID = 3
ADMINS = (('Matt Caldwell', 'matt.caldwell@gmail.com'), )
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'matt.caldwell@gmail.com'
EMAIL_HOST_PASSWORD = 'fIw2qnuRJO2JYLvtuyKumA'
INSTALLED_APPS += ('storages', )
TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader', ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')), )
AWS_ACCESS_KEY_ID = 'AKIAJSWBP2Y3VOSVNGBQ'
AWS_SECRET_ACCESS_KEY = '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'
CELERITY_STATICFILES_BUCKET = 'pegasus-static'
CELERITY_MEDIAFILES_BUCKET = 'pegasus-media'
AWS_S3_URL_PROTOCOL = ''
DEFAULT_FILE_STORAGE = 'pegasus.storage.CelerityMediaFilesStorage'
STATICFILES_STORAGE = 'pegasus.storage.CelerityStaticFilesStorage'
STATIC_URL = '{s3_protocol}//{s3_bucket}.s3.amazonaws.com/'.format(s3_protocol=AWS_S3_URL_PROTOCOL, s3_bucket=CELERITY_STATICFILES_BUCKET)
CACHES = {'default': {'BACKEND': 'redis_cache.RedisCache', 
             'LOCATION': '54.173.1.254:6379', 
             'OPTIONS': {'DB': 1}, 
             'TIMEOUT': 86400}, 
 'decorated': {'BACKEND': 'redis_cache.RedisCache', 
               'LOCATION': '54.173.1.254:6379', 
               'OPTIONS': {'DB': 2}, 
               'TIMEOUT': 3600}, 
 'staticfiles': {'BACKEND': 'redis_cache.RedisCache', 
                 'LOCATION': '54.173.1.254:6379', 
                 'OPTIONS': {'DB': 3}, 
                 'TIMEOUT': 0}}
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 
             'NAME': 'pegasus_prod_1', 
             'HOST': 'pegasus-prod-1.ccxuxmyvkfqh.us-east-1.rds.amazonaws.com', 
             'USER': 'pegasus_db', 
             'PASSWORD': 'FKxgsXOkrcTu', 
             'PORT': '5432', 
             'CONN_MAX_AGE': 900}}
HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine', 
             'URL': 'https://bofur-us-east-1.searchly.com:80/', 
             'INDEX_NAME': 'pegasus', 
             'TIMEOUT': 300, 
             'INCLUDE_SPELLING': True, 
             'BATCH_SIZE': 100, 
             'KWARGS': {'http_auth': 'site:49970ebb2fda35c0ed81e481a07477ef'}}}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'