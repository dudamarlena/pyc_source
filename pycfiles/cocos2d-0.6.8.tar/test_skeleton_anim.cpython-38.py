# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_skeleton_anim.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1413 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.3, s, t 0.6, s, t 1, s, q'
tags = 'skeleton, BitmapSkin, Animate'
try:
    import cPickle as pickle
except Exception:
    import pickle
else:
    import cocos
    import cocos.director as director
    from cocos.sprite import Sprite
    from cocos import skeleton
    import pyglet, sample_skeleton, sample_skin

    class TestLayer(cocos.layer.Layer):

        def __init__(self):
            super(TestLayer, self).__init__()
            x, y = director.get_window_size()
            self.skin = skeleton.BitmapSkin(sample_skeleton.skeleton, sample_skin.skin)
            self.add(self.skin)
            x, y = director.get_window_size()
            self.skin.position = (x // 2, y // 2)
            anim = pickle.load(open('SAMPLE.anim', 'rb'))
            self.skin.do(cocos.actions.Repeat(skeleton.Animate(anim)))


    def main():
        director.init()
        test_layer = TestLayer()
        bg_layer = cocos.layer.ColorLayer(255, 255, 255, 255)
        main_scene = cocos.scene.Scene()
        main_scene.add(bg_layer, z=(-10))
        main_scene.add(test_layer, z=10)
        director.run(main_scene)


    if __name__ == '__main__':
        main()