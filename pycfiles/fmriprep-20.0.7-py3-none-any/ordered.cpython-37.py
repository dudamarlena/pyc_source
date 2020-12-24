# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/toml/ordered.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 378 bytes
from collections import OrderedDict
from pip._vendor.toml import TomlEncoder
from pip._vendor.toml import TomlDecoder

class TomlOrderedDecoder(TomlDecoder):

    def __init__(self):
        super(self.__class__, self).__init__(_dict=OrderedDict)


class TomlOrderedEncoder(TomlEncoder):

    def __init__(self):
        super(self.__class__, self).__init__(_dict=OrderedDict)