# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jessemaitland/PycharmProjects/commando/venv/lib/python3.6/site-packages/rambo/config/config.py
# Compiled at: 2019-09-25 01:54:58
# Size of source mod 2**32: 393 bytes
import yaml
from pathlib import Path

def load_config(path=None):
    if not path:
        config_filename = 'rambo.yml'
        path = Path().cwd().absolute() / config_filename
    return yaml.safe_load(path.open())


def load_config_template():
    config_filename = 'config_template.yml'
    path = Path(__file__).absolute().parent / config_filename
    return yaml.safe_load(path.open())