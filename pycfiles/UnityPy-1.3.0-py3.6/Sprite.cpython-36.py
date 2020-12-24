# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Sprite.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 5052 bytes
from enum import IntEnum
from .Mesh import BoneWeights4, SubMesh, VertexData
from .NamedObject import NamedObject
from .PPtr import PPtr
from ..export import SpriteHelper

class Sprite(NamedObject):

    @property
    def image(self):
        return SpriteHelper.get_image_from_sprite(self)

    def __init__(self, reader):
        super().__init__(reader=reader)
        version = self.version
        self.m_Rect = reader.read_rectangle_f()
        self.m_Offset = reader.read_vector2()
        if version[0] > 4 or version[0] == 4 and version[1] >= 5:
            self.m_Border = reader.read_vector4()
        self.m_PixelsToUnits = reader.read_float()
        if version[0] > 5 or version[0] == 5 and version[1] > 4 or version[0] == 5 and version[1] == 4 and version[2] >= 2 or version[0] == 5 and version[1] == 4 and version[2] == 1 and self.build_type.IsPatch and version[3] >= 3:
            self.m_Pivot = reader.read_vector2()
        self.m_Extrude = reader.read_u_int()
        if version[0] > 5 or version[0] == 5 and version[1] >= 3:
            self.m_IsPolygon = reader.read_boolean()
            reader.align_stream()
        if version[0] >= 2017:
            first = reader.read_bytes(16)
            second = reader.read_long()
            self.m_RenderDataKey = (first, second)
            self.m_AtlasTags = reader.read_string_array()
            self.m_SpriteAtlas = PPtr(reader)
        self.m_RD = SpriteRenderData(reader)
        if version[0] >= 2017:
            m_PhysicsShapeSize = reader.read_int()
            self.m_PhysicsShape = [reader.read_vector2_array() for _ in range(m_PhysicsShapeSize)]


class SecondarySpriteTexture:

    def __init__(self, reader):
        self.texture = PPtr(reader)
        self.name = reader.read_string_to_null()


class SpritePackingRotation(IntEnum):
    kSPRNone = (0, )
    kSPRFlipHorizontal = (1, )
    kSPRFlipVertical = (2, )
    kSPRRotate180 = (3, )
    kSPRRotate90 = 4


class SpritePackingMode(IntEnum):
    kSPMTight = (0, )
    kSPMRectangle = 1


class SpriteSettings:

    def __init__(self, reader):
        settingsRaw = reader.read_u_int()
        self.packed = settingsRaw & 1
        self.packingMode = SpritePackingMode(settingsRaw >> 1 & 1)
        self.packingRotation = SpritePackingRotation(settingsRaw >> 2 & 15)


class SpriteVertex:

    def __init__(self, reader):
        version = reader.version
        self.pos = reader.read_vector3()
        if version[0] < 4 or version[0] == 4 and version[1] <= 3:
            self.uv = reader.read_vector2()


class SpriteRenderData:

    def __init__(self, reader):
        version = reader.version
        self.texture = PPtr(reader)
        if version[0] > 5 or version[0] == 5 and version[1] >= 2:
            self.alphaTexture = PPtr(reader)
        else:
            if version[0] >= 2019:
                secondaryTexturesSize = reader.read_int()
                self.secondaryTextures = [SecondarySpriteTexture(reader) for _ in range(secondaryTexturesSize)]
            if version[0] > 5 or version[0] == 5 and version[1] >= 6:
                m_SubMeshesSize = reader.read_int()
                self.m_SubMeshes = [SubMesh(reader) for _ in range(m_SubMeshesSize)]
                self.m_IndexBuffer = reader.read_bytes(reader.read_int())
                reader.align_stream()
                self.m_VertexData = VertexData(reader)
            else:
                verticesSize = reader.read_int()
                self.vertices = [SpriteVertex(reader) for _ in range(verticesSize)]
                self.indices = reader.read_u_short_array()
                reader.align_stream()
        if version[0] >= 2018:
            self.m_Bindpose = reader.read_matrix_array()
            if version[0] == 2018:
                if version[1] < 2:
                    m_SourceSkinSize = reader.read_int()
                    self.m_SourceSkin = [BoneWeights4(reader)]
        self.textureRect = reader.read_rectangle_f()
        self.textureRectOffset = reader.read_vector2()
        if version[0] > 5 or version[0] == 5 and version[1] >= 6:
            self.atlasRectOffset = reader.read_vector2()
        self.settingsRaw = SpriteSettings(reader)
        if version[0] > 4 or version[0] == 4 and version[1] >= 5:
            self.uvTransform = reader.read_vector4()
        if version[0] >= 2017:
            self.downscaleMultiplier = reader.read_float()