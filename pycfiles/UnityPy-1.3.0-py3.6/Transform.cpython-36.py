# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Transform.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 477 bytes
from .Component import Component
from .PPtr import PPtr

class Transform(Component):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.local_rotation = reader.read_quaternion()
        self.local_position = reader.read_vector3()
        self.local_scale = reader.read_vector3()
        children_count = reader.read_int()
        self.children = [PPtr(reader) for _ in range(children_count)]
        self.father = PPtr(reader)