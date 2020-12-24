# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/config.py
# Compiled at: 2014-10-17 04:10:07
"""
This is the config for titanOSX
"""
import ConfigParser, inspect
from os.path import dirname, abspath, join, isfile
from sys import argv, exit

def titanConfig(config_file, titanosxpath):
    config = {'main': {'debug': False, 
                'datastore': join(titanosxpath, 'titan.db'), 
                'logstore': join(titanosxpath, 'logs'), 
                'monitorstore': join(titanosxpath, 'monitors'), 
                'reportstore': join(titanosxpath, 'reports')}, 
       'reporting': {'type': 'http', 
                     'enabled': False, 
                     'target': '', 
                     'token': 'default'}, 
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