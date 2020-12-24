# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/web-portfolio/web_portfolio/tests/config.py
# Compiled at: 2015-08-23 23:50:25
"""
WebPortfolio

Base config file

"""
import os
CWD = os.path.dirname(__file__)

class BaseConfig(object):
    """
    Base configuration
    """
    APPLICATION_ADMIN_EMAIL = ''
    APPLICATION_NAME = ''
    APPLICATION_URL = ''
    APPLICATION_VERSION = '0.0.1'
    APPLICATION_EMAIL = ''
    APPLICATION_GOOGLE_ANALYTICS_ID = ''
    APPLICATION_PAGINATION_PER_PAGE = 25
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_S3_BUCKET_NAME = ''
    SQL_URI = 'sqlite:////%s/data/db.db' % CWD
    REDIS_URI = None
    ASSETS_DELIVERY_METHOD = None
    ASSETS_DELIVERY_DOMAIN = None
    SESSION_URI = None
    STORAGE_PROVIDER = 'LOCAL'
    STORAGE_KEY = AWS_ACCESS_KEY_ID
    STORAGE_SECRET = AWS_SECRET_ACCESS_KEY
    STORAGE_CONTAINER = '%s/data/uploads' % CWD
    STORAGE_SERVER = True
    MAILER_SENDER = APPLICATION_EMAIL
    MAILER_REPLY_TO = APPLICATION_EMAIL
    MAILER_TEMPLATE = '%s/data/mailer-templates' % CWD
    MAILER_TEMPLATE_CONTEXT = {'site_name': APPLICATION_NAME, 
       'site_url': APPLICATION_URL}
    CACHE_TYPE = 'simple'
    CACHE_REDIS_URL = ''
    CACHE_DIR = ''
    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = ''
    RECAPTCHA_SECRET_KEY = ''
    MODULE_USER_ACCOUNT_ENABLE_LOGIN = True
    MODULE_USER_ACCOUNT_ENABLE_SIGNUP = True
    MODULE_USER_ACCOUNT_RESET_PASSWORD_METHOD = 'TOKEN'
    MODULE_USER_ACCOUNT_ENABLE_OAUTH_LOGIN = False
    MODULE_USER_ACCOUNT_OAUTH_PROVIDERS = {'Facebook': {'consumer_key': '', 
                    'consumer_secret': ''}, 
       'Google': {'consumer_key': '', 
                  'consumer_secret': ''}, 
       'Twitter': {'consumer_key': '', 
                   'consumer_secret': ''}}
    MODULE_CONTACT_PAGE_EMAIL = APPLICATION_EMAIL
    MODULE_MAINTENANCE_PAGE_ON = False


class Test(BaseConfig):
    pass


class Development(BaseConfig):
    """
    Config for development environment
    """
    SERVER_NAME = None
    DEBUG = True
    SECRET_KEY = 'PLEASE CHANGE ME'


class Production(BaseConfig):
    """
    Config for Production environment
    """
    SERVER_NAME = None
    DEBUG = False
    SECRET_KEY = None