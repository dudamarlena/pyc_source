# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/config_parser.py
# Compiled at: 2019-12-29 16:28:04
# Size of source mod 2**32: 937 bytes
import json, os

class ConfigParser:

    def __init__(self, config_dir):
        self.config_dir = config_dir

    def create_config_for_adapter(self, adapter_id, adapter_type):
        base_config = json.load(open('{}/{}_config.json'.format(self.config_dir, adapter_id)))
        general_config = json.load(open('{}/agent_config.json'.format(self.config_dir)))
        full_adapter_conf = {}
        full_adapter_conf['adapter'] = base_config['adapter']
        full_adapter_conf['adapter']['adapter_type'] = adapter_type
        full_adapter_conf['metadata'] = general_config['metadata']
        full_adapter_conf['options'] = general_config['options']
        return full_adapter_conf

    def add_new_adapter(self, adapter_config):
        pass