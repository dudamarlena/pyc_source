# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\AssetBundle.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 701 bytes
from .NamedObject import NamedObject
from .PPtr import PPtr

class AssetInfo:

    def __init__(self, reader):
        self.preload_index = reader.read_int()
        self.preload_size = reader.read_int()
        self.asset = PPtr(reader)


class AssetBundle(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        preload_table_size = reader.read_int()
        self.preload_table = [PPtr(reader) for _ in range(preload_table_size)]
        container_size = reader.read_int()
        self.container = {}
        for i in range(container_size):
            key = reader.read_aligned_string()
            self.container[key] = AssetInfo(reader)