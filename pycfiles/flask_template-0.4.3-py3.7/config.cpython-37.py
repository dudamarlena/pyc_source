# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/simple/proj/config.py
# Compiled at: 2020-03-11 03:42:34
# Size of source mod 2**32: 937 bytes
import logging, os, datetime

class Config(object):
    DEBUG = False
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    LOG_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@host/db?charset=utf8'
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    LOG_LEVEL = logging.WARNING


def get_config_class():
    env = os.environ.get('proj_env'.upper(), 'dev').lower()
    if env == 'prod':
        return ProductionConfig
    return DevelopmentConfig


CONF = get_config_class()