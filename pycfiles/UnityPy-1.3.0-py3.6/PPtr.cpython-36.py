# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\PPtr.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 4452 bytes
from ..streams import EndianBinaryReader, EndianBinaryWriter

class PPtr:

    def __init__(self, reader: EndianBinaryReader):
        self.index = -2
        self.file_id = reader.read_int()
        self.path_id = reader.read_int() if reader.version2 < 14 else reader.read_long()
        self.assets_file = reader.assets_file

    def __getattr__(self, key):
        manager = None
        if self.file_id == 0:
            manager = self.assets_file
        else:
            if self.file_id > 0:
                if self.file_id - 1 < len(self.assets_file.externals):
                    if self.index == -2:
                        external_name = self.assets_file.externals[(self.file_id - 1)].name
                        files = self.assets_file.parent.files
                        if external_name not in files:
                            external_name = external_name.upper()
                        manager = self.assets_file.parent.files[external_name]
        if manager:
            if self.path_id in manager.objects:
                self = manager.objects[self.path_id]
                return getattr(self, key)
        raise NotImplementedError('PPtr')

    def __repr__(self):
        return self.__class__.__name__

    def __bool__(self):
        return False


def save_ptr(obj, writer: EndianBinaryWriter):
    if isinstance(obj, PPtr):
        writer.write_int(obj.file_id)
        writer.write_int(obj.path_id)
    else:
        writer.write_int(0)
        writer.write_int(obj.path_id)