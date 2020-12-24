# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/components/interface.py
# Compiled at: 2020-05-11 13:21:42
# Size of source mod 2**32: 841 bytes
""" The Generic component interface.
"""
import os, json
from mamba_server.utils.component import generate_component_configuration
SETTINGS_FILE = 'settings.json'
COMPONENT_CONFIG_FILE = 'component.config.json'

class ComponentInterface:

    def __init__(self, settings_folder, config_folder, context):
        super(ComponentInterface, self).__init__()
        self._context = context
        self._configuration = {}
        with open(os.path.join(settings_folder, SETTINGS_FILE)) as (f):
            settings_description = json.load(f)
        with open(os.path.join(config_folder, COMPONENT_CONFIG_FILE)) as (f):
            file_config = json.load(f)
        self._configuration = generate_component_configuration(settings=settings_description,
          config_file=file_config)