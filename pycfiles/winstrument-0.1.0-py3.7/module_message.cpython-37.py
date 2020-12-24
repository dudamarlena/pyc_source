# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\data\module_message.py
# Compiled at: 2019-08-23 17:51:28
# Size of source mod 2**32: 1351 bytes
from datetime import datetime
import winstrument.utils as utils
import os

class ModuleMessage:

    def __init__(self, module, target, data, time=datetime.now().strftime('%Y-%m-%d %T')):
        self.module = module
        self.time = time
        self.target = target
        self.data = data

    def flatten(self):
        fulldata = {'module':self.module,  'time':self.time,  'target':self.target}
        fulldata.update(self.data)
        return fulldata

    def truncate_path(self):
        """
        Return a copy of the message with the target path elipsized
        """
        return ModuleMessage(self.module, utils.elipsize_path(self.target), self.data, self.time)