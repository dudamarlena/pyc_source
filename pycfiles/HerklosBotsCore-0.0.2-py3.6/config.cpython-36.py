# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botcore/config/config.py
# Compiled at: 2018-04-01 06:36:57
# Size of source mod 2**32: 265 bytes
import json

def load_config(config_file='config/config.json'):
    try:
        with open(config_file) as (json_data_file):
            config = json.load(json_data_file)
        return config
    except Exception:
        raise Exception('Error when load config')