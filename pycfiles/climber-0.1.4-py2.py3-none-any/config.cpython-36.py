# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/climb/config.py
# Compiled at: 2015-05-24 06:11:57
# Size of source mod 2**32: 867 bytes
import os, configparser
from climb.exceptions import ConfigNotFound
DEFAULT_CONFIG_PATHS = [
 './{name}.conf',
 '~/.{name}.conf',
 '/etc/{name}/{name}.conf']
config = configparser.ConfigParser()

def load_config(name):
    config.clear()
    paths = [path.format(name=name) for path in DEFAULT_CONFIG_PATHS]
    for config_path in paths:
        if _read_config(config_path):
            break
    else:
        raise ConfigNotFound('Could not find {name}.conf'.format(name))


def load_config_file(path):
    config.clear()
    if not _read_config(path):
        raise ConfigNotFound('Could not load {}'.format(path))


def _read_config(path):
    config_path = os.path.expanduser(path)
    if os.path.isfile(config_path) and os.access(config_path, os.R_OK):
        config.read(config_path)
        return True
    else:
        return False