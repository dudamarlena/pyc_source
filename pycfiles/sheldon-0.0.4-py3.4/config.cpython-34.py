# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon/config.py
# Compiled at: 2015-11-19 22:52:29
# Size of source mod 2**32: 2638 bytes
"""
@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
import os, yaml
from sheldon.utils import logger

class Config:

    def __init__(self, prefix='SHELDON_'):
        """
        Load config from environment variables.

        :param prefix: string, all needed environment variables
                            starts from it.
                            Default - 'SHELDON_'. So, environment
                            variables will be looking like:
                            'SHELDON_BOT_NAME', 'SHELDON_TWITTER_KEY'
        :return:
        """
        self.variables = {}
        for variable in os.environ:
            if variable.startswith(prefix):
                self.variables[variable] = os.environ[variable]
                continue

        self._set_installed_plugins()

    def get(self, variable, default_value=None):
        """
        Get variable value from environment

        :param variable: string, needed variable
        :param default_value: string, value that returns if
                              variable is not set
        :return: variable value
        """
        if variable not in self.variables:
            return default_value
        return self.variables[variable]

    def _set_installed_plugins(self):
        """
        Create list of installed plugins from installed_plugins.txt
        :return:
        """
        plugins_file = open('installed_plugins.txt')
        self.installed_plugins = plugins_file.readlines()


class ModuleConfig:
    __doc__ = '\n    Config class for each module: plugins and adapters\n    '

    def __init__(self, data):
        """
        Create config object for plugin or adapter

        :param data: dict, result of yaml.load()
        :return:
        """
        self.name = data['name']
        self.description = data['description']
        self.variables = data['config']
        self._data = data


def parse_config(module):
    """
    Parse module (plugin/adapter) config in __doc__

    :param module: module object
    :return: ModuleConfig object
    """
    if not hasattr(module, '__doc__'):
        logger.error_message('__doc__ config not found in {}'.format(module))
        return
    config_text = module.__doc__
    try:
        config_data = yaml.load(config_text)
    except yaml.scanner.ScannerError as error:
        logger.error_message('Error while reading {} config \n {}'.format(module, error.__traceback__))
        return

    config = ModuleConfig(config_data)
    return config