# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/aegis_model/util/config.py
# Compiled at: 2020-01-27 21:51:56
# Size of source mod 2**32: 1187 bytes
import json, os
CONFIG_FOLDER_NAME = 'config'

class ConfigFileReader(object):

    def __init__(self):
        pass

    def read_api_config(self, config_file='config.json'):
        config_params = self.read_config_in_default_folder(config_file)
        return config_params['wows_api']

    def read_mongo_config(self, config_file='config.json'):
        config_params = self.read_config_in_default_folder(config_file)
        return config_params['mongo']

    def read_config_in_default_folder(self, config_file):
        config_file_path = self._get_config_folder_path()
        return self.read_config(file_dir=config_file_path, file_name=config_file)

    @classmethod
    def read_config(cls, file_dir, file_name):
        file_path = os.path.join(file_dir, file_name)
        with open(file_path) as (config_data):
            database_config_json = json.load(config_data)
        return database_config_json

    @staticmethod
    def _get_config_folder_path():
        current_path = os.path.dirname(os.path.realpath(__file__))
        project_root_path = os.path.dirname(os.path.dirname(current_path))
        return os.path.join(project_root_path, CONFIG_FOLDER_NAME)