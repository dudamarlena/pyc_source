# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """SingleConfig"""

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