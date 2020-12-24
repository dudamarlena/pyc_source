# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.munaro/workspace/brokerpackager/brokerpackager/installer.py
# Compiled at: 2017-08-16 14:26:29
# Size of source mod 2**32: 589 bytes
from .managers.python import PyManager
from .managers.r import RManager

class Installer(object):

    def __init__(self, config={}):
        python_log_file = config.get('python', {}).get('log_file', '')
        r_log_file = config.get('r', {}).get('log_file', '')
        self.managers = {'python':PyManager(python_log_file),  'r':RManager(r_log_file)}

    def install(self, config):
        for manager_name in self.managers:
            manager = self.managers[manager_name]
            manager.install_list(config.get(manager_name, {}).get('paths', []), config.get(manager_name, {}))