# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/naphatkrit/Dropbox/Documents/code/easyci/easyci/user_config.py
# Compiled at: 2015-09-04 22:36:51
import os, yaml

class ConfigFormatError(Exception):
    pass


class ConfigNotFoundError(Exception):
    pass


_default_config = {'tests': [], 'collect_results': [], 'history_limit': 100}
_config_types = {'tests': list, 
   'collect_results': list, 
   'history_limit': int}

def load_user_config(vcs):
    """Load the user config

    Args:
        vcs (easyci.vcs.base.Vcs) - the vcs object for the current project

    Returns:
        dict - the config

    Raises:
        ConfigFormatError
        ConfigNotFoundError
    """
    config_path = os.path.join(vcs.path, 'eci.yaml')
    if not os.path.exists(config_path):
        raise ConfigNotFoundError
    with open(config_path, 'r') as (f):
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError:
            raise ConfigFormatError

    if not isinstance(config, dict):
        raise ConfigFormatError
    for k, v in _default_config.iteritems():
        config.setdefault(k, v)

    for k, v in _config_types.iteritems():
        if not isinstance(config[k], v):
            raise ConfigFormatError

    return config