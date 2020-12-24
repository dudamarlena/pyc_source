# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\MovieTexture.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 353 bytes
from .PPtr import PPtr
from .Texture import Texture

class MovieTexture(Texture):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.Loop = reader.read_boolean()
        reader.align_stream()
        self.AudioClip = PPtr(reader)
        self.m_MovieData = reader.read_bytes(reader.read_int())