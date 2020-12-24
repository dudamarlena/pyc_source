# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pydbwrapper/config.py
# Compiled at: 2020-01-30 14:30:52
# Size of source mod 2**32: 1347 bytes
__doc__ = 'PyDBWrapper Configuration'
import json, os, psycopg2
import DBUtils.PooledDB as PooledDB

class ConfigurationNotFoundError(Exception):
    """ConfigurationNotFoundError"""
    pass


class InvalidConfigurationError(Exception):
    """InvalidConfigurationError"""
    pass


class Config(object):
    """Config"""
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

        elif config_dict:
            self.data = config_dict
        self.print_sql = self.data.pop('print_sql') if 'print_sql' in self.data else False
        self.pool = PooledDB(psycopg2, **self.data)

    @staticmethod
    def instance(configuration_file='/etc/pydbwrapper/config.json', config_dict=None):
        """Get singleton instance of Configuration"""
        if Config._Config__instance is None:
            Config._Config__instance = Config(configuration_file, config_dict)
        return Config._Config__instance