# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComicThief/config.py
# Compiled at: 2017-02-05 15:23:56
# Size of source mod 2**32: 849 bytes
from configparser import ConfigParser
import os
from pathlib import Path, PurePath
CONFIG = 'default.ini'

class WithConfig:

    def __init__(self):
        self.config = get_config(CONFIG)
        self.img_dir = self.config['SETTINGS'].get('img_dir', 'img')


class SingleConfig:
    __doc__ = 'Singleton forcing that there is only one configuration instance used'

    class Config(ConfigParser):

        def get_config(self, name):
            self.read(name)
            return self

    instance = None

    def __init__(self):
        if not SingleConfig.instance:
            SingleConfig.instance = SingleConfig.Config()

    def __getattr__(self, item):
        return getattr(self.instance, item)


def get_config(name):
    config = SingleConfig()
    return config.get_config(str(Path(Path(__file__).parent, name)))