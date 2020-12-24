# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/commands/settoken.py
# Compiled at: 2019-08-09 05:52:36
# Size of source mod 2**32: 389 bytes
import sys
sys.path.append('..')
from dobg.helper.confighandler import ConfigHandler

def set_token(args):
    """ Sets a Digital Ocean authentication token in configuration file """
    answer = input('Are you sure you want to set this token? (yes/no): ')
    print()
    if answer in ('y', 'Y', 'yes', 'YES', 'Yes'):
        ConfigHandler.set_config_setting('token', args.token)