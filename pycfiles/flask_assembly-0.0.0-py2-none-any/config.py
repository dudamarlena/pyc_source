# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/devlab/new/t1/application/config.py
# Compiled at: 2019-08-23 22:08:52
"""
CONFIGURATION

Class based config file, where each class is an environment:
ie: Dev = Development, Prod=Production, ...

Flasik: Global Configuration

Global config shared by all applications

The method allow multiple configuration

By default, it is expecting the Dev and Prod, but you can add your class
which extends from BaseConfig

- Access in templates
You have the ability to access these config in your template
just use the global variable `config`
ie:
    {{ config.APPLICATION_NAME }}

"""
from . import get_var_path, ROOT_DIR, VAR_DIR

class BaseConfig(object):
    """
    Base Configuration.
    """
    APPLICATION_NAME = 'Flasik'
    APPLICATION_URL = ''
    APPLICATION_VERSION = '0.0.1'
    GOOGLE_ANALYTICS_ID = ''
    ADMIN_EMAIL = None
    CONTACT_EMAIL = None
    PAGINATION_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 2097152
    COMPRESS_HTML = False
    DATETIME_TIMEZONE = 'US/Eastern'
    DATETIME_FORMAT = {'default': 'MM/DD/YYYY', 
       'date': 'MM/DD/YYYY', 
       'datetime': 'MM/DD/YYYY hh:mm a', 
       'time': 'hh:mm a', 
       'long_datetime': 'dddd, MMMM D, YYYY hh:mm a'}
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_S3_BUCKET_NAME = ''
    AWS_REGION_NAME = 'us-east-1'
    DB_URL = 'sqlite:////%s/db.db' % VAR_DIR
    REDIS_URL = None
    ASSETS_DELIVERY_METHOD = None
    ASSETS_DELIVERY_DOMAIN = None
    SESSION_URL = None
    STORAGE_PROVIDER = 'LOCAL'
    STORAGE_KEY = AWS_ACCESS_KEY_ID
    STORAGE_SECRET = AWS_SECRET_ACCESS_KEY
    STORAGE_REGION_NAME = AWS_REGION_NAME
    STORAGE_CONTAINER = get_var_path('uploads')
    STORAGE_SERVER = True
    STORAGE_SERVER_URL = 'files'
    STORAGE_UPLOAD_FILE_PROPS = {'image': {'extensions': [
                              'jpg', 'png', 'gif', 'jpeg'], 
                 'public': True}, 
       'profile-image': {'prefix': 'profile-image/', 
                         'extensions': [
                                      'jpg', 'png', 'gif', 'jpeg'], 
                         'public': True}}
    MAIL_SENDER = ADMIN_EMAIL
    MAIL_REPLY_TO = ADMIN_EMAIL
    MAIL_TEMPLATE = get_var_path('mail-templates')
    MAIL_TEMPLATE_CONTEXT = {'params': {'site_name': APPLICATION_NAME, 
                  'site_url': APPLICATION_URL}}
    CACHE_TYPE = 'simple'
    CACHE_REDIS_URL = ''
    CACHE_DIR = ''
    RECAPTCHA_ENABLED = False
    RECAPTCHA_SITE_KEY = ''
    RECAPTCHA_SECRET_KEY = ''


class Dev(BaseConfig):
    """
    Config for development environment
    """
    SERVER_NAME = None
    DEBUG = True
    SECRET_KEY = 'PLEASE CHANGE ME'


class Prod(BaseConfig):
    """
    Config for Production environment
    """
    SERVER_NAME = None
    DEBUG = False
    SECRET_KEY = None
    COMPRESS_HTML = True