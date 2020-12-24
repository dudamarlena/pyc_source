# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\bsn_base.py
# Compiled at: 2020-04-20 02:32:30
# Size of source mod 2**32: 187 bytes
from bsn_sdk_py.client.config import Config

class BsnBase(object):

    def __init__(self):
        pass

    def set_config(self, config: Config):
        self.config = config