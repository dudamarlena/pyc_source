# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Animator.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 1642 bytes
from .Behaviour import Behaviour
from .PPtr import PPtr

class Animator(Behaviour):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.avatar = PPtr(reader)
        self.controller = PPtr(reader)
        self.culling_mode = reader.read_int()
        if self.version[0] > 4 or self.version[0] == 4 and self.version[1] > 4:
            self.update_mode = reader.read_int()
        self.m_ApplyRootMotion = reader.read_boolean()
        if self.version[0] == 4:
            if self.version[1] >= 5:
                reader.align_stream()
        if self.version[0] >= 5:
            self.linear_velocity_blending = reader.read_boolean()
            reader.align_stream()
        if self.version[0] < 4 or self.version[0] == 4 and self.version[1] < 5:
            self.animate_physics = reader.read_boolean()
        if self.version[0] > 4 or self.version[0] == 4 and self.version[1] >= 3:
            self.has_transform_hierarchy = reader.read_boolean()
        if self.version[0] > 4 or self.version[0] == 4 and self.version[1] >= 5:
            self.allow_constant_clip_sampling_optimization = reader.read_boolean()
        if 4 < self.version[0] < 2018:
            reader.align_stream()
        if self.version[0] >= 2018:
            self.m_KeepAnimatorControllerStateOnDisable = reader.read_boolean()
            reader.align_stream()