# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bass/config.py
# Compiled at: 2015-09-12 07:34:17
# Size of source mod 2**32: 1681 bytes
"""
bass.config
-----
Objects and functions related to configuration.
"""
import argparse
from os import getcwd
from os.path import exists, isfile, join
from . import setting
from .common import read_yaml_file
config_default = {'extension': 'extension', 
 'follow_links': False, 
 'ignore': '.?*', 
 'input': 'input', 
 'output': 'output', 
 'layout': 'layout'}

def read_config():
    """read configuration file, define global settings"""
    config_file = 'config'
    config = config_default.copy()
    if exists(config_file):
        if isfile(config_file):
            config.update(read_yaml_file(config_file))
    setting.ignore = config['ignore'].split()
    if config_default['ignore'] not in setting.ignore:
        setting.ignore.append(config_default['ignore'])
    setting.project = getcwd()
    setting.extension = join(setting.project, config['extension'])
    setting.follow_links = config['follow_links']
    setting.input = join(setting.project, config['input'])
    setting.layout = join(setting.project, config['layout'])
    setting.output = join(setting.project, config['output'])


def parse_cmdline():
    """parse command line, return parsed argument list"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--build', help='build', action='store_true', default=False)
    parser.add_argument('-c', '--create', help='create', action='store_true', default=False)
    parser.add_argument('-d', '--debug', help='debug', action='store_true', default=False)
    parser.add_argument('-s', '--server', help='server', action='store_true')
    return parser.parse_args()