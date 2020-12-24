# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/policytool/configfile.py
# Compiled at: 2019-05-23 11:08:11
import json, os, platform
from collections import OrderedDict

def _find_default_config():
    if platform.system() != 'Windows':
        user_config = os.path.expanduser('~/.config/cobra-policytool/config.json')
        if os.path.exists(user_config):
            return user_config
        if os.path.exists('/etc/cobra-policytool/config.json'):
            return '/etc/cobra-policytool/config.json'
    else:
        user_config = os.path.expanduser('~\\cobra-policytool\\config.json')
        if os.path.exists(user_config):
            return user_config


class JSONPropertiesFile:

    def __init__(self, config_file_path, default_config={}):
        if config_file_path is None:
            config_file_path = _find_default_config()
        self.default_config = default_config
        self.properties = default_config
        if not config_file_path.endswith('.json'):
            raise ConfigFileError('Must be a JSON file: %s' % config_file_path)
        if os.path.exists(config_file_path):
            with open(config_file_path) as (config_file):
                self.properties.update(json.load(config_file, object_pairs_hook=OrderedDict))
        return

    def get(self, environment):
        if environment is None:
            return self.properties
        else:
            for env in self.properties['environments']:
                if env['name'] == environment:
                    return env

            return self.default_config


class ConfigFileError(Exception):
    pass