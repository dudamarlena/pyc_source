# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bogdan/projects/personal/configuration.py/configuration_py/parsers/json_parser.py
# Compiled at: 2017-03-29 10:11:23
import json
from configuration_py.parsers.base_parser import BaseConfigParser

class JSONParser(BaseConfigParser):
    extensions = ('json', )

    def parse(self, file_content, context={}):
        config_dict = json.loads(file_content)
        if not config_dict or type(config_dict) is not dict:
            raise EnvironmentError('Config file does not contain config variables')
        return config_dict