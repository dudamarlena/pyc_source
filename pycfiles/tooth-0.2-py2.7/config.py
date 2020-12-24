# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tooth/config.py
# Compiled at: 2015-04-29 20:46:50
__author__ = 'Tom James Holub'
from ConfigParser import ConfigParser
import os.path
DEFAULT_PATH = None

def set_default_config_file_path(path):
    global DEFAULT_PATH
    DEFAULT_PATH = path


def get_default_config_file_path():
    return DEFAULT_PATH


class Config:

    def __init__(self, path=None):
        path = path or get_default_config_file_path()
        if path is None:
            raise ValueError('Path not selected. Use Config(path=...) or config.set_default_config_file_path(...)')
        if not os.path.isfile(path):
            raise ValueError('No file found at %s' % path)
        self.config_parser = ConfigParser()
        self.config_parser.read(path)
        return

    def get(self, section, name, value_type=str):
        value = self.config_parser.get(section, name)
        value = value.split('#')[0]
        value = value.strip(' \t')
        if section == 'path':
            if not os.path.exists(value):
                os.makedirs(value)
            return value
        if value == 'None':
            return
        else:
            if value_type == int:
                return int(value)
            if value_type == bool:
                if value == 'True':
                    return True
                if value == 'False':
                    return False
                raise ValueError('Cannot convert config value to bool, use either True or False. %s at %s:%s' % (value, section, name))
            else:
                if value_type == list:
                    return value.split(',')
                if value_type == str:
                    return value
                raise ValueError('value_type must be int, bool, str, list')
            return