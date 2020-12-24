# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_interpreter_layer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 606 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'PythonInterpreterLayer'
import cocos
import cocos.director as director
import pyglet

def main():
    director.init(resizable=True)
    interpreter_layer = cocos.layer.PythonInterpreterLayer()
    main_scene = cocos.scene.Scene(interpreter_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()