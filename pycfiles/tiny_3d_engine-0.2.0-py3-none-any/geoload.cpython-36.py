# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/examples/geoload.py
# Compiled at: 2020-04-20 18:58:54
# Size of source mod 2**32: 459 bytes
""" The Basic script to import a geo or ply file"""
import sys
from tiny_3d_engine import Engine3D, load_file_as_scene
__all__ = [
 'spawngeo']

def spawngeo(file_):
    """Script to import a file"""
    scene = load_file_as_scene(file_,
      prefix='essa1',
      color='#ffffff')
    scene.add_axes()
    test = Engine3D(scene, title=(str(file_)))
    test.render()
    test.mainloop()


if __name__ == '__main__':
    spawngeo(sys.argv[1])