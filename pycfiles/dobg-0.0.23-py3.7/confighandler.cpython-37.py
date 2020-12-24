# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/helper/confighandler.py
# Compiled at: 2019-07-25 12:09:10
# Size of source mod 2**32: 2024 bytes
import json, os, sys
sys.path.append('..')
from dobg.exceptions.configexceptions import MissingTokenException

class ConfigHandler:
    config_file = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/dobg-config.json'

    @classmethod
    def get_config_setting(cls, key):
        """ Gets property from config dictionary"""
        config_data = cls.get_config_data()
        if key == 'token':
            token = config_data.get(key, False)
            if token == False:
                raise MissingTokenException
        return config_data.get(key, False)

    @classmethod
    def set_config_setting(cls, key, value):
        """ Sets property in config dictionary """
        config_data = cls.get_config_data()
        config_data[key] = value
        if cls.set_config_data(config_data):
            print('Changes made in config file:\n\n{}: {}\n'.format(key, value))

    @classmethod
    def get_config_data(cls):
        """ Opens config file, reading and returning data from it as a dictionary """
        mode = 'r' if os.path.exists(cls.config_file) else 'w+'
        try:
            with open(cls.config_file, mode) as (json_file):
                if mode == 'w+':
                    data = {}
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                    json_file.seek(0)
                return json.load(json_file)
        except:
            print('Error: could not open config file for reading!')
            sys.exit()

    @classmethod
    def set_config_data(cls, data):
        """ Opens config file and rewriting it with data dictionary dumped as json """
        try:
            with open(cls.config_file, 'w') as (json_file):
                json.dump(data, json_file, ensure_ascii=False, indent=4)
                return True
        except:
            print('Error: could not open config file for writing!')
            sys.exit()