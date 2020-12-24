# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/config.py
# Compiled at: 2019-10-18 10:04:55
# Size of source mod 2**32: 1077 bytes
import os
from PyQt5.QtCore import QSettings

class Params(object):
    __doc__ = '\n    Params Configuration\n    This class load all settings from .ini file\n    '

    def __init__(self, file_):
        self.file = file_
        dirx = os.path.abspath(os.path.join(__file__, '..', '..'))
        if os.name == 'posix':
            homex = 'HOME'
            dirconfig = '.tryton'
        else:
            if os.name == 'nt':
                homex = 'USERPROFILE'
                dirconfig = 'AppData/Local/tryton'
            else:
                HOME_DIR = os.getenv(homex)
                default_dir = os.path.join(HOME_DIR, dirconfig)
                if os.path.exists(default_dir):
                    config_file = os.path.join(default_dir, self.file)
                else:
                    config_file = os.path.join(dirx, self.file)
            if not os.path.exists(config_file):
                config_file = self.file
            settings = QSettings(config_file, QSettings.IniFormat)
            self.params = {}
            for key in settings.allKeys():
                if key[0] == '#':
                    continue
                self.params[key] = settings.value(key, None)