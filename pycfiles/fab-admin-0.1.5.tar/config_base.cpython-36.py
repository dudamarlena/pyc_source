# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\temp\sandbox\config_base.py
# Compiled at: 2020-02-04 02:27:43
# Size of source mod 2**32: 7157 bytes
"""
fabadmin common config module.

Created on 2020-02-04 15:27:42.

"""
import os, imp
from fab_admin import config
from flask_appbuilder.const import *
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))
version = imp.load_source('version', os.path.join(basedir, 'version.py'))
try:
    config_local = imp.load_source('config_local', os.path.join(basedir, 'config_local.py'))
except Exception:
    config_local = None

class config(config.config):
    __doc__ = 'Customize your config.'
    SECRET_KEY = '\x02\x039b611a6539f8a65fa94818c32f33493d937b2b3\x01\x02\\e\\y\\y\\h'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_ECHO = False
    CSRF_ENABLED = True
    APP_MODE = 'DEV'
    APP_NAME = version.APP_NAME
    APP_VERSION = '%s:%s' % (APP_MODE, version.VERSION_STRING)
    APP_DESC = version.DESCRIPTION
    APP_AUTHOR = version.AUTHOR_NAME
    AUTH_TYPE = AUTH_LDAP
    AUTH_ROLE_ADMIN = 'Admin'
    AUTH_ROLE_PUBLIC = 'Public'
    AUTH_LDAP_SERVER = 'ldap://your.ldap.server:389/'
    AUTH_LDAP_SEARCH = 'ou=people,ou=intranet,dc=company,dc=com'
    AUTH_LDAP_EMAIL_FIELD = 'mail'
    AUTH_LDAP_UID_FIELD = 'your_uid'
    AUTH_LDAP_FIRSTNAME_FIELD = 'givenName'
    AUTH_LDAP_LASTNAME_FIELD = 'sn'
    AUTH_USER_REGISTRATION = True
    AUTH_USER_REGISTRATION_ROLE = AUTH_ROLE_PUBLIC
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_FOLDER = 'translations'
    LANGUAGES = {'en':{'flag':'gb', 
      'name':'English'}, 
     'pt':{'flag':'pt', 
      'name':'Portuguese'}, 
     'pt_BR':{'flag':'br', 
      'name':'Pt Brazil'}, 
     'es':{'flag':'es', 
      'name':'Spanish'}, 
     'de':{'flag':'de', 
      'name':'German'}, 
     'zh':{'flag':'cn', 
      'name':'Chinese'}, 
     'ru':{'flag':'ru', 
      'name':'Russian'}, 
     'pl':{'flag':'pl', 
      'name':'Polish'}}
    UPLOAD_FOLDER = basedir + '/app/static/uploads/'
    IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/'
    IMG_UPLOAD_URL = '/static/uploads/'
    SESSION_COOKIE_NAME = '%s_session' % version.APP_NAME.lower()
    SESSION_KEY_PREFIX = version.APP_NAME.lower()
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    FLASK_LOG_LEVEL = 'DEBUG'
    LOG_LEVEL = 'DEBUG'
    LOG_NAME = version.APP_NAME.lower()
    FLASK_LOG_PATH = '%s/logs/%s.log' % (basedir, version.APP_NAME.lower())
    ADDON_MANAGERS = [
     'fab_addon_autodoc.manager.AutoDocManager']
    TEMPLATES_AUTO_RELOAD = True
    AUTO_UPDATE_PERM = os.environ.get('AUTO_UPDATE_PERM', True)
    USER_TYPE_LOCAL = 'local'
    USER_TYPE_LDAP = 'ldap'
    COMMON_PERMISSIONS = [
     'userapikey']
    COMMON_LOCAL_USER_PERMISSION = ['userinfoedit', 'resetmypassword']
    COMMON_LOCAL_USER_VIEW = ['UserInfoEditView', 'ResetMyPasswordView']
    REDISSN = 'mymaster'
    REDISPASS = os.environ.get('REDIS_PASSWORD', config_local.REDISPASS if config_local else None)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis+sentinel://:{0}@localhost:26379/{1}/2'.format(REDISPASS, REDISSN))
    REDIS_DECODE_RESPONSES = True
    SSE_REDIS_URL = os.environ.get('SSE_REDIS_URL', 'redis+sentinel://:{0}@localhost:26379/{1}/1'.format(REDISPASS, REDISSN))
    SECURITY_CLEANUP = True
    SPOOLER_PATH = '{0}/logs/spooler'.format(basedir)
    EMAIL_DEFAULT_FROM = ('admin', 'youradmin@comapny.com')
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.com')
    EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
    FAB_AUTH_REDIS_CACHE = True
    FAB_AUTH_REDIS_CACHE_SCOPE = 'REST'
    FAB_AUTH_REDIS_RPV_KEY = 'fab:rpv'
    FAB_AUTH_REDIS_UAPIK_KEY = 'fab:uapik'
    FAB_AUTH_KEY_REPLACE_PATTERN = '[\'|\\"]'