# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scottblevins/git/impression/impression/settings.py
# Compiled at: 2016-07-22 12:07:57
import os, tempfile
db_file = tempfile.NamedTemporaryFile()

class Config(object):
    SECRET_KEY = 'REPLACE THIS KEY ASAP'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_NO_NULL_WARNING = True
    DEBUG = True


class ProdConfig(Config):
    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../impression/impression.db'
    CACHE_TYPE = 'simple'
    DEBUG = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../impression/impression.db'
    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False