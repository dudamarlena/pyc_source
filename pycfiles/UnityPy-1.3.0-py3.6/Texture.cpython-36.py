# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Texture.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 840 bytes
from .NamedObject import NamedObject
from ..streams import EndianBinaryWriter

class Texture(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        if self.version[0] > 2017 or self.version[0] == 2017 and self.version[1] >= 3:
            self.forced_fallback_format = reader.read_int()
            self.downscale_fallback = reader.read_boolean()
            reader.align_stream()

    def save(self, writer):
        super().save(writer)
        if self.version[0] > 2017 or self.version[0] == 2017 and self.version[1] >= 3:
            writer.write_int(self.forced_fallback_format)
            writer.write_boolean(self.downscale_fallback)
            writer.align_stream()