# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\EditorExtension.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 684 bytes
from .Object import Object
from .PPtr import PPtr, save_ptr
from ..enums import BuildTarget
from ..streams import EndianBinaryWriter, EndianBinaryReader

class EditorExtension(Object):

    def __init__(self, reader):
        super().__init__(reader=reader)
        if self.platform == BuildTarget.NoTarget:
            self.prefab_parent_object = PPtr(reader)
            self.prefab_internal = PPtr(reader)

    def save(self, writer):
        super().save(writer, intern_call=True)
        if self.platform == BuildTarget.NoTarget:
            save_ptr(self.prefab_parent_object)
            save_ptr(self.prefab_internal)