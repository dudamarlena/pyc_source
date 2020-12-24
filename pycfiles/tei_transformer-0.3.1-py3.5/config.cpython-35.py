# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tei_transformer/config.py
# Compiled at: 2016-02-15 00:49:28
# Size of source mod 2**32: 452 bytes
import os, yaml
with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as (f):
    config = yaml.load(f)

def update_config(curdir):
    """Update config with custom settings."""
    custom_settings = os.path.join(str(curdir), 'resources', 'config.yaml')
    try:
        with open(custom_settings) as (f):
            custom_settings = yaml.load(f)
        config.extend(custom_settings)
    except FileNotFoundError:
        pass