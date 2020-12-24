# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\ConfigReader\ConfigReader.py
# Compiled at: 2019-06-15 04:39:25
# Size of source mod 2**32: 656 bytes
import yaml
from abc import ABC, abstractmethod
from py_buildsystem.common import logger

class ConfigReader(ABC):

    def __init__(self, config_yaml_file):
        self.read_config_file(config_yaml_file)
        self._check_config()

    def read_config_file(self, config_yaml_file):
        try:
            with open(config_yaml_file, 'r') as (config_file):
                self.configuration = yaml.load(config_file)
        except FileNotFoundError:
            logger.error('Given configuration file does not exist.')
            exit(-1)

    @abstractmethod
    def _check_config(self):
        pass