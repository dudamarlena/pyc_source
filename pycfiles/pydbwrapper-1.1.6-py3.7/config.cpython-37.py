# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pydbwrapper/config.py
# Compiled at: 2020-01-30 14:30:52
# Size of source mod 2**32: 1347 bytes
"""PyDBWrapper Configuration"""
import json, os, psycopg2
import DBUtils.PooledDB as PooledDB

class ConfigurationNotFoundError(Exception):
    __doc__ = 'Configuration file was not found'


class InvalidConfigurationError(Exception):
    __doc__ = 'Configuration is not a valid json file'


class Config(object):
    __doc__ = 'Configuration object'
    _Config__instance = None

    def __init__(self, configuration_file=None, config_dict=None):
        if configuration_file:
            if not os.path.exists(configuration_file):
                raise ConfigurationNotFoundError()
            with open(configuration_file, 'r') as (config):
                try:
                    self.data = json.loads(config.read())
                except json.decoder.JSONDecodeError as ex:
                    try:
                        raise InvalidConfigurationError(ex)
                    finally:
                        ex = None
                        del ex

        else:
            if config_dict:
                self.data = config_dict
        self.print_sql = self.data.pop('print_sql') if 'print_sql' in self.data else False
        self.pool = PooledDB(psycopg2, **self.data)

    @staticmethod
    def instance(configuration_file='/etc/pydbwrapper/config.json', config_dict=None):
        """Get singleton instance of Configuration"""
        if Config._Config__instance is None:
            Config._Config__instance = Config(configuration_file, config_dict)
        return Config._Config__instance