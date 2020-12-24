# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjharries/Code/@wizardsoftheweb/py-rofi-bus/py_rofi_bus/components/mixins/has_config.py
# Compiled at: 2018-06-03 14:06:06
# Size of source mod 2**32: 273 bytes
from py_rofi_bus.components import Config

class HasConfig(object):

    def __init__(self, config=None, *args, **kwargs):
        if config is None:
            self.config = Config(*args, **kwargs)
        else:
            self.config = config