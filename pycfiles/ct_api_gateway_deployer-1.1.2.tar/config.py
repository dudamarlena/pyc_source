# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/config.py
# Compiled at: 2014-08-23 23:34:58
__doc__ = '\nThis is the config for ctznOSX\n'
import ConfigParser, inspect
from os.path import dirname, abspath, join, isfile
from sys import argv, exit

def ctznConfig(config_file, ctznosxpath):
    config = {'main': {'debug': False, 
                'datastore': join(ctznosxpath, 'ctznosx.db'), 
                'logstore': join(ctznosxpath, 'logs'), 
                'monitorstore': join(ctznosxpath, 'monitors'), 
                'reportstore': join(ctznosxpath, 'reports')}, 
       'reporting': {'type': 'http', 
                     'enabled': False, 
                     'target': ''}, 
       'watcher': {'enabled': 'true', 
                   'timeout': 3, 
                   'send_every': 60}}
    if isfile(config_file):
        cp = ConfigParser.ConfigParser()
        cp.read(config_file)
        for section in cp.sections():
            for option in cp.options(section):
                config[section][option] = cp.get(section, option)

    else:
        print '!! NOTICE - Using default configuration'
    return config