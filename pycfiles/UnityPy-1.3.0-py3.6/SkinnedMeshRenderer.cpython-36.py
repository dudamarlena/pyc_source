# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\SkinnedMeshRenderer.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 857 bytes
from .PPtr import PPtr
from .Renderer import Renderer

class SkinnedMeshRenderer(Renderer):

    def __init__(self, reader):
        super().__init__(reader=reader)
        version = self.version
        self.m_Quality = reader.read_int()
        self.m_UpdateWhenOffscreen = reader.read_boolean()
        self.m_SkinNormals = reader.read_boolean()
        reader.align_stream()
        if version[0] == 2:
            if version[1] < 6:
                self.m_DisableAnimationWhenOffscreen = PPtr(reader)
        self.m_Mesh = PPtr(reader)
        m_BonesSize = reader.read_int()
        self.m_Bones = [PPtr(reader) for _ in range(m_BonesSize)]
        if version[0] > 4 or version[0] == 4 and version[1] >= 3:
            self.m_BlendShapeWeights = reader.read_float_array()