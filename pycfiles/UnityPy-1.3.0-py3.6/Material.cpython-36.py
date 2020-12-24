# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Material.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 2444 bytes
from .NamedObject import NamedObject
from .PPtr import PPtr

class Material(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        version = self.version
        self.m_Shader = PPtr(reader)
        if version[0] == 4:
            if version[1] >= 1:
                self.m_ShaderKeywords = reader.read_string_array()
        if version[0] >= 5:
            self.m_ShaderKeywords = reader.read_aligned_string()
            self.m_LightmapFlags = reader.read_u_int()
        if version[0] > 5 or version[0] == 5 and version[1] >= 6:
            self.m_EnableInstancingVariants = reader.read_boolean()
            reader.align_stream()
        if version[0] > 4 or version[0] == 4 and version[1] >= 3:
            self.m_CustomRenderQueue = reader.read_int()
        if version[0] > 5 or version[0] == 5 and version[1] >= 1:
            stringTagMapSize = reader.read_int()
            self.stringTagMap = {}
            for _ in range(stringTagMapSize):
                first = reader.read_aligned_string()
                second = reader.read_aligned_string()
                self.stringTagMap[first] = second

        if version[0] > 5 or version[0] == 5 and version[1] >= 6:
            self.disabledShaderPasses = reader.read_string_array()
        self.m_SavedProperties = UnityPropertySheet(reader)


class UnityTexEnv:

    def __init__(self, reader):
        self.m_Texture = PPtr(reader)
        self.m_Scale = reader.read_vector2()
        self.m_Offset = reader.read_vector2()


class UnityPropertySheet:

    def __init__(self, reader):
        m_TexEnvsSize = reader.read_int()
        self.m_TexEnvs = {}
        for i in range(m_TexEnvsSize):
            key = reader.read_aligned_string()
            self.m_TexEnvs[key] = UnityTexEnv(reader)

        m_FloatsSize = reader.read_int()
        self.m_Floats = {}
        for i in range(m_FloatsSize):
            key = reader.read_aligned_string()
            self.m_Floats[key] = reader.read_float()

        m_ColorsSize = reader.read_int()
        self.m_Colors = {}
        for i in range(m_ColorsSize):
            key = reader.read_aligned_string()
            self.m_Colors[key] = reader.read_color4()