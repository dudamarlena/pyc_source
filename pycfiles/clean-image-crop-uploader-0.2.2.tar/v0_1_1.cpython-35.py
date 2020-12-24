# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/updates/versions/v0_1_1.py
# Compiled at: 2018-03-25 09:00:03
# Size of source mod 2**32: 750 bytes
__doc__ = '0.1.1 Update.'
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
    """V0_1_1"""

    def up(self, config: dict) -> dict:
        """Upgrade config file."""
        config['path'] = [_update_path(x) for x in config['path']]
        return config

    def down(self, config: dict) -> dict:
        """Downgrade config file."""
        config['path'] = [_downgrade_path(x) for x in config['path']]
        return config