# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/controller/json.py
# Compiled at: 2015-06-17 12:23:17
# Size of source mod 2**32: 211 bytes
from .base import Controller

class JsonController(Controller):
    __doc__ = '\n    Controller which will return context as json.\n    '
    renderer = 'json'

    def _create_context(self):
        self.context = {}