# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\scenes\sequences.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3118 bytes
__doc__ = ' '
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from cocos.scene import Scene
import cocos.director as director
__all__ = [
 'SequenceScene']

class SequenceScene(Scene):
    """SequenceScene"""

    def __init__(self, *scenes):
        super(SequenceScene, self).__init__()
        self.scenes = scenes
        self.p = 0

    def on_enter(self):
        if self.p >= len(self.scenes):
            director.pop()
        else:
            director.push(self.scenes[self.p])
        self.p += 1