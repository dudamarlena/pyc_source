# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\settings.py
# Compiled at: 2020-03-06 16:27:20
# Size of source mod 2**32: 2883 bytes
"""
settings - define default, test and production settings

see http://flask.pocoo.org/docs/1.0/config/?highlight=production#configuration-best-practices
"""
import logging
from loutilities.configparser import getitems

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_BINDS = {'users': 'sqlite:///:memory:'}
    LOGGING_LEVEL_FILE = logging.INFO
    LOGGING_LEVEL_MAIL = logging.ERROR
    SECURITY_TRACKABLE = True
    SECURITY_DEFAULT_REMEMBER_ME = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'dev.localhost'
    SECRET_KEY = '<test secret key>'
    LOGIN_DISABLED = False


class RealDb(Config):

    def __init__(self, configfiles):
        if type(configfiles) == str:
            configfiles = [
             configfiles]
        config = {}
        for configfile in configfiles:
            config.update(getitems(configfile, 'database'))

        userdbuser = config['userdbuser']
        userpassword = config['userdbpassword']
        userdbserver = config['userdbserver']
        userdbname = config['userdbname']
        userdb_uri = 'mysql://{uname}:{pw}@{server}/{dbname}'.format(uname=userdbuser, pw=userpassword, server=userdbserver, dbname=userdbname)
        self.SQLALCHEMY_BINDS = {'users': userdb_uri}


class Development(RealDb):
    DEBUG = True


class Production(RealDb):
    pass