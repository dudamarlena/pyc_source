# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\bsn_base.py
# Compiled at: 2020-04-20 02:32:30
# Size of source mod 2**32: 187 bytes
from bsn_sdk_py.client.config import Config

class BsnBase(object):

    def __init__(self):
        pass

    def set_config(self, config: Config):
        self.config = config