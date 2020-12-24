# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\AnimatorOverrideController.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 550 bytes
from .PPtr import PPtr
from .RuntimeAnimatorController import RuntimeAnimatorController

class AnimationClipOverride:

    def __init__(self, reader):
        self.original_clip = PPtr(reader)
        self.override_clip = PPtr(reader)


class AnimatorOverrideController(RuntimeAnimatorController):

    def __init__(self, reader):
        super().__init__(reader=reader)
        self.controller = PPtr(reader)
        num_overrides = reader.read_int()
        self.clips = [AnimationClipOverride(reader) for i in range(num_overrides)]