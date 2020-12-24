# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\__init__.py
# Compiled at: 2020-01-21 23:28:16
# Size of source mod 2**32: 5351 bytes
__doc__ = 'a framework for building 2D games, demos, and other graphical/interactive applications.\n\nMain Features\n-------------\n\n    * Flow control: Manage the flow control between different scenes in an easy way\n    * Sprites: Fast and easy sprites\n    * Actions: Just tell sprites what you want them to do. Composable actions like move, rotate, scale and much more\n    * Effects: Effects like waves, twirl, lens and much more\n    * Tiled Maps: Support for rectangular and hexagonal tiled maps\n    * Collision: Basic pure python support for collisions\n    * Transitions: Move from scene to scene with style\n    * Menus: Built in classes to create menus\n    * Text Rendering: Label and HTMLLabel with action support\n    * Documentation: Programming Guide + API Reference + Video Tutorials + Lots of simple tests showing how to use it\n    * Built-in Python Interpreter: For debugging purposes\n    * BSD License: Just use it\n    * Pyglet Based: No external dependencies\n    * OpenGL Based: Hardware Acceleration\n\nhttp://python.cocos2d.org\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
__version__ = '0.6.8'
__author__ = 'cocos2d team'
version = __version__
import sys, os, pyglet
pyglet.resource.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources'))
pyglet.resource.reindex()
parts = pyglet.version.split('.')
p_major, p_med, p_step = parts
bad_pyglet_version = True
if p_major != '1':
    print('This cocos version needs pyglet >= 1.4.10 and < 2.0')
elif p_med not in ('4', '5'):
    print('This cocos version needs pyglet >= 1.4.10 or 1.5.x')
elif p_med == '4' and int(p_step) < 10:
    print('This cocos version needs pyglet >= 1.4.10 or 1.5.x')
else:
    bad_pyglet_version = False
if bad_pyglet_version:
    raise Exception('\n*** bad pyglet version, found version %s ***\n' % pyglet.version)
try:
    unittesting = os.environ['cocos_utest']
except KeyError:
    unittesting = False
else:
    del os
    del pyglet
    if sys.platform == 'win32':
        major, minor = sys.version_info[0:2]
        if not major == 2:
            if not major == 3 or minor < 4:
                import imp
                try:
                    dummy, sdl_lib_path, dummy = imp.find_module('pygame')
                    del dummy
                except ImportError:
                    sdl_lib_path = None

        else:
            import importlib
            try:
                spec = importlib.util.find_spec('pygame')
                sdl_lib_path = spec.submodule_search_locations[0]
            except Exception:
                sdl_lib_path = None

    if not unittesting:
        from cocos import cocosnode
        from cocos import actions
        from cocos import director
        from cocos import layer
        from cocos import menu
        from cocos import sprite
        from cocos import path
        from cocos import scene
        from cocos import grid
        from cocos import text
        from cocos import camera
        from cocos import draw
        from cocos import skeleton
        from cocos import rect
        from cocos import tiles