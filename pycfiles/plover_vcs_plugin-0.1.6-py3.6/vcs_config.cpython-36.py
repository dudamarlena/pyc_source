# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/vcs_config.py
# Compiled at: 2020-04-03 19:43:25
# Size of source mod 2**32: 1015 bytes
import json, os
from typing import List
from plover.config import CONFIG_DIR
CONFIG_FILE = os.path.join(CONFIG_DIR, 'plover_vcs.json')

class VcsConfig:

    def __init__(self, vcs: str='', dictionaries: List[str]=None):
        self.vcs = vcs
        self.dictionaries = [] if dictionaries is None else dictionaries

    def fromJson(json):
        return VcsConfig(vcs=(json.get('vcs', '')), dictionaries=(json.get('dictionaries', [])))


class VcsConfigManager:

    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            self.config = VcsConfig()
        else:
            with open(CONFIG_FILE, 'r') as (f):
                self._VcsConfigManager__config = VcsConfig.fromJson(json.load(f))

    @property
    def config(self) -> VcsConfig:
        return self._VcsConfigManager__config

    @config.setter
    def config(self, config: VcsConfig):
        self._VcsConfigManager__config = config
        with open(CONFIG_FILE, 'w') as (f):
            json.dump(config.__dict__, f)


CONFIG_MANAGER = VcsConfigManager()