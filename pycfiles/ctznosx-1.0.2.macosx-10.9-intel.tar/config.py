# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/config.py
# Compiled at: 2014-08-23 23:34:58
"""
This is the config for ctznOSX
"""
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