# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/config.py
# Compiled at: 2012-08-03 08:35:35
from xdg import BaseDirectory
import os, ConfigParser

class Configuration(object):

    @staticmethod
    def Path():
        path = os.path.join(BaseDirectory.xdg_config_home, 'snurtle')
        if not os.path.isdir(path):
            os.mkdir(path)
        path = os.path.join(path, 'config.ini')
        return path

    @staticmethod
    def Load():
        path = Configuration.Path()
        config = ConfigParser.RawConfigParser()
        if not os.path.isfile(path):
            config.add_section('Global')
            Configuration.SetHost(config, '')
            Configuration.SetLogin(config, '')
            Configuration.SetSecure(config, 0)
        else:
            config.read(path)
        return config

    @staticmethod
    def GetHost(config):
        if 'host' in config.options('Global'):
            hostname = config.get('Global', 'host')
        else:
            hostname = ''
        return hostname

    @staticmethod
    def SetHost(config, value):
        config.set('Global', 'host', value)

    @staticmethod
    def GetLogin(config):
        return config.get('Global', 'login')

    @staticmethod
    def SetLogin(config, value):
        config.set('Global', 'login', value)

    @staticmethod
    def GetSecure(config):
        if 'secure' in config.items('Global'):
            return config.get('Global', 'secure')
        else:
            return 0

    @staticmethod
    def SetSecure(config, value):
        config.set('Global', 'secure', value)

    @staticmethod
    def Save(config):
        path = Configuration.Path()
        wfile = open(path, 'wb')
        if wfile:
            config.write(wfile)
            wfile.close