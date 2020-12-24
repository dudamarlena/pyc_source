# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/ConfigFile.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 1010 bytes
import yaml, os

class ConfigFile:
    path: str
    config = {}
    config: {}

    def __init__(self):
        self.path = self.get_path()
        if os.path.isfile(self.path):
            with open(self.path, 'r') as (ymlconfig):
                self.config = yaml.load(ymlconfig, yaml.SafeLoader)

    def config_key_exists(self, *keys):
        return (self.keys_exists)(self.config, *keys)

    @staticmethod
    def get_path():
        return os.path.expandvars(os.path.join('$HOME', '.onepassword-tools.yml'))

    def get_section(self, section):
        if section in self.config.keys():
            return self.config[section]

    @staticmethod
    def keys_exists(element, *keys):
        if type(element) is not dict:
            return False
        if len(keys) == 0:
            return False
        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False

        return True