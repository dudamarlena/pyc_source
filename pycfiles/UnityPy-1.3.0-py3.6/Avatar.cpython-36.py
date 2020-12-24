# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Avatar.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 5474 bytes
from .AnimationClip import xform
from .NamedObject import NamedObject

class Avatar(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.m_AvatarSize = reader.read_u_int()
        self.m_Avatar = AvatarConstant(reader)
        numTOS = reader.read_int()
        self.m_TOS = {}
        for _ in range(numTOS):
            key = reader.read_u_int()
            self.m_TOS[key] = reader.read_aligned_string()

    def FindBonePath(self, hash):
        return self.m_TOS[hash]


class Node:

    def __init__(self, reader):
        self.m_ParentId = reader.read_int()
        self.m_AxesId = reader.read_int()


class Limit:

    def __init__(self, reader):
        version = reader.version
        if version[0] > 5 or version[0] == 5 and version[1] >= 4:
            self.m_Min = reader.read_vector3()
            self.m_Max = reader.read_vector3()
        else:
            self.m_Min = reader.read_vector4()
            self.m_Max = reader.read_vector4()


class Axes:

    def __init__(self, reader):
        version = reader.version
        self.m_PreQ = reader.read_vector4()
        self.m_PostQ = reader.read_vector4()
        if version[0] > 5 or version[0] == 5 and version[1] >= 4:
            self.m_Sgn = reader.read_vector3()
        else:
            self.m_Sgn = reader.read_vector4()
        self.m_Limit = Limit(reader)
        self.m_Length = reader.read_float()
        self.m_Type = reader.read_u_int()


class Skeleton:

    def __init__(self, reader):
        numNodes = reader.read_int()
        self.m_Node = [Node(reader) for _ in range(numNodes)]
        self.m_ID = reader.read_u_int_array()
        numAxes = reader.read_int()
        self.m_AxesArray = [Axes(reader) for _ in range(numAxes)]


class SkeletonPose:

    def __init__(self, reader):
        numXforms = reader.read_int()
        self.m_X = [xform(reader) for _ in range(numXforms)]


class Hand:

    def __init__(self, reader):
        self.m_HandBoneIndex = reader.read_int_array()


class Handle:

    def __init__(self, reader):
        self.m_X = xform(reader)
        self.m_ParentHumanIndex = reader.read_u_int()
        self.m_ID = reader.read_u_int()


class Collider:

    def __init__(self, reader):
        self.m_X = xform(reader)
        self.m_Type = reader.read_u_int()
        self.m_XMotionType = reader.read_u_int()
        self.m_YMotionType = reader.read_u_int()
        self.m_ZMotionType = reader.read_u_int()
        self.m_MinLimitX = reader.read_float()
        self.m_MaxLimitX = reader.read_float()
        self.m_MaxLimitY = reader.read_float()
        self.m_MaxLimitZ = reader.read_float()


class Human:

    def __init__(self, reader):
        version = reader.version
        self.m_RootX = xform(reader)
        self.m_Skeleton = Skeleton(reader)
        self.m_SkeletonPose = SkeletonPose(reader)
        self.m_LeftHand = Hand(reader)
        self.m_RightHand = Hand(reader)
        if version[0] < 2018 or version[0] == 2018 and version[1] < 2:
            numHandles = reader.read_int()
            self.m_Handles = [Handle(reader) for _ in range(numHandles)]
            numColliders = reader.read_int()
            self.m_ColliderArray = [Collider(reader) for _ in range(numColliders)]
        self.m_HumanBoneIndex = reader.read_int_array()
        self.m_HumanBoneMass = reader.read_float_array()
        if version[0] < 2018 or version[0] == 2018 and version[1] < 2:
            self.m_ColliderIndex = reader.read_int_array()
        self.m_Scale = reader.read_float()
        self.m_ArmTwist = reader.read_float()
        self.m_ForeArmTwist = reader.read_float()
        self.m_UpperLegTwist = reader.read_float()
        self.m_LegTwist = reader.read_float()
        self.m_ArmStretch = reader.read_float()
        self.m_LegStretch = reader.read_float()
        self.m_FeetSpacing = reader.read_float()
        self.m_HasLeftHand = reader.read_boolean()
        self.m_HasRightHand = reader.read_boolean()
        if version[0] > 5 or version[0] == 5 and version[1] >= 2:
            self.m_HasTDoF = reader.read_boolean()
        reader.align_stream()


class AvatarConstant:

    def __init__(self, reader):
        version = reader.version
        self.m_AvatarSkeleton = Skeleton(reader)
        self.m_AvatarSkeletonPose = SkeletonPose(reader)
        if version[0] > 4 or version[0] == 4 and version[1] >= 3:
            self.m_DefaultPose = SkeletonPose(reader)
            self.m_SkeletonNameIDArray = reader.read_u_int_array()
        self.m_Human = Human(reader)
        self.m_HumanSkeletonIndexArray = reader.read_int_array()
        if version[0] > 4 or version[0] == 4 and version[1] >= 3:
            self.m_HumanSkeletonReverseIndexArray = reader.read_int_array()
        self.m_RootMotionBoneIndex = reader.read_int()
        self.m_RootMotionBoneX = xform(reader)
        if version[0] > 4 or version[0] == 4 and version[1] >= 3:
            self.m_RootMotionSkeleton = Skeleton(reader)
            self.m_RootMotionSkeletonPose = SkeletonPose(reader)
            self.m_RootMotionSkeletonIndexArray = reader.read_int_array()