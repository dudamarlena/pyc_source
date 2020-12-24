# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Renderer.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 4023 bytes
from .Component import Component
from .PPtr import PPtr

class StaticBatchInfo:

    def __init__(self, reader):
        self.firstSubMesh = reader.read_u_short()
        self.subMeshCount = reader.read_u_short()


class Renderer(Component):

    def __init__(self, reader):
        super().__init__(reader=reader)
        version = self.version
        if version[0] < 5:
            self.m_Enabled = reader.read_boolean()
            self.m_CastShadows = reader.read_boolean()
            self.m_ReceiveShadows = reader.read_boolean()
            self.m_LightmapIndex = reader.read_byte()
        else:
            if version[0] > 5 or version[0] == 5 and version[1] >= 4:
                self.m_Enabled = reader.read_boolean()
                self.m_CastShadows = reader.read_byte()
                self.m_ReceiveShadows = reader.read_byte()
                if version[0] > 2017 or version[0] == 2017 and version[0] >= 2:
                    self.m_DynamicOccludee = reader.read_byte()
                self.m_MotionVectors = reader.read_byte()
                self.m_LightProbeUsage = reader.read_byte()
                self.m_ReflectionProbeUsage = reader.read_byte()
                if version[0] > 2019 or version[0] == 2019 and version[0] >= 3:
                    self.m_RayTracingMode = reader.ReadByte()
                reader.align_stream()
            else:
                self.m_Enabled = reader.read_boolean()
                reader.align_stream()
                self.m_CastShadows = reader.read_byte()
                self.m_ReceiveShadows = reader.read_boolean()
                reader.align_stream()
            if version[0] >= 2018:
                self.m_RenderingLayerMask = reader.read_u_int()
            if version[0] > 2018 or version[0] == 2018 and version[1] >= 3:
                self.m_RendererPriority = reader.read_int()
            self.m_LightmapIndex = reader.read_u_short()
            self.m_LightmapIndexDynamic = reader.read_u_short()
        if version[0] >= 3:
            self.m_LightmapTilingOffset = reader.read_vector4()
        elif version[0] >= 5:
            self.m_LightmapTilingOffsetDynamic = reader.read_vector4()
        else:
            m_MaterialsSize = reader.read_int()
            self.m_Materials = [PPtr(reader) for _ in range(m_MaterialsSize)]
            if version[0] < 3:
                self.m_LightmapTilingOffset = reader.read_vector4()
            else:
                if version[0] > 5 or version[0] == 5 and version[1] >= 5:
                    self.m_StaticBatchInfo = StaticBatchInfo(reader)
                else:
                    self.m_SubsetIndices = reader.read_u_int_array()
                self.m_StaticBatchRoot = PPtr(reader)
            if version[0] > 5 or version[0] == 5 and version[1] >= 4:
                self.m_ProbeAnchor = PPtr(reader)
                self.m_LightProbeVolumeOverride = PPtr(reader)
            elif version[0] > 3 or version[0] == 3 and version[1] >= 5:
                self.m_UseLightProbes = reader.read_boolean()
                reader.align_stream()
                if version[0] >= 5:
                    self.m_ReflectionProbeUsage = reader.read_int()
                self.m_LightProbeAnchor = PPtr(reader)
        if version[0] > 4 or version[0] == 4 and version[1] >= 3:
            if version[0] == 4:
                if version[1] == 3:
                    self.m_SortingLayer = reader.read_short()
            else:
                self.m_SortingLayerID = reader.read_u_int()
            self.m_SortingOrder = reader.read_short()
            reader.align_stream()