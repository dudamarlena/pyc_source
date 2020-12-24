# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\scenes\sequences.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3118 bytes
""" """
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from cocos.scene import Scene
import cocos.director as director
__all__ = [
 'SequenceScene']

class SequenceScene(Scene):
    __doc__ = 'A Scene used to play a sequence of scenes one after another.\n\n    Arguments:\n        *scenes (Scene): argument list with the scenes to play.\n\n    The playing goes from first arg to last arg.\n\n    For each scene, scene.on_enter is not called until it becomes active.\n\n    Use director.pop to advance to the next scene.\n\n    director.pop when the last scene is playing removes that scene and the\n    SequenceScene from the scene stack.\n\n    Example use case: running a intro scene before the main menu scene::\n\n        director.run(SequenceScene(intro(), menuGame()))\n\n    '

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