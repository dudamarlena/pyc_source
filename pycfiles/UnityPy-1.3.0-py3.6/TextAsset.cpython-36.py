# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\TextAsset.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 801 bytes
from .NamedObject import NamedObject
from ..streams import EndianBinaryWriter, EndianBinaryReader

class TextAsset(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.script = reader.read_bytes(reader.read_int())

    @property
    def text(self):
        return self.script.decode('utf8')

    @text.setter
    def text(self, val):
        self.script = val.encode('utf8')

    def save(self, writer=None):
        if writer is None:
            writer = EndianBinaryWriter(endian=(self.reader.endian))
        super().save(writer)
        writer.write_int(len(self.script))
        writer.write_bytes(self.script)
        writer.align_stream()
        self.reader.data = writer.bytes