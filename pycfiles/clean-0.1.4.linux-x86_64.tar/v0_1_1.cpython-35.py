# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/updates/versions/v0_1_1.py
# Compiled at: 2018-03-25 09:00:03
# Size of source mod 2**32: 750 bytes
"""0.1.1 Update."""
from .version import Version

def _update_path(path_config: dict) -> dict:
    if 'use_meta_tag' not in path_config:
        path_config['use_meta_tag'] = False
    return path_config


def _downgrade_path(path_config: dict) -> dict:
    if 'use_meta_tag' in path_config:
        del path_config['use_meta_tag']
    return path_config


class V0_1_1(Version):
    __doc__ = 'Version 0.1.1 Update.'

    def up(self, config: dict) -> dict:
        """Upgrade config file."""
        config['path'] = [_update_path(x) for x in config['path']]
        return config

    def down(self, config: dict) -> dict:
        """Downgrade config file."""
        config['path'] = [_downgrade_path(x) for x in config['path']]
        return config