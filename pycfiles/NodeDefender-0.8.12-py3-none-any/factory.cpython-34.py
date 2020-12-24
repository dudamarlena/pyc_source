# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/config/factory.py
# Compiled at: 2018-02-22 04:21:18
# Size of source mod 2**32: 525 bytes
import NodeDefender

class DefaultConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'key'
    SECRET_SALT = 'salt'
    PORT = 5000
    SELF_REGISTRATION = True
    WTF_CSRF_ENABLED = False
    DATABASE = False
    REDIS = False
    LOGGING = False
    MAIL = False
    CELERY = False


class TestingConfig(DefaultConfig):
    TESTING = True
    DATABASE = False
    LOGGING = False
    MAIL = False
    CELERY = False