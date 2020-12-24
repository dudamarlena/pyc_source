# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/examples/rabbit.py
# Compiled at: 2020-04-22 18:51:27
# Size of source mod 2**32: 812 bytes
import pkg_resources
from tiny_3d_engine import Engine3D, load_file_as_scene

def spawnrabbit(shading, version=4):
    """Test the engine on the Standford rabbit"""
    if version == '4':
        rabbit = './bun_zipper_res4.ply'
    else:
        if version == '3':
            rabbit = './bun_zipper_res3.ply'
        else:
            if version == '2':
                rabbit = './bun_zipper_res2.ply'
            else:
                raise NotImplementedError()
    rabbitfile = pkg_resources.resource_filename(__name__, rabbit)
    scene = load_file_as_scene(rabbitfile)
    scene.add_axes()
    test = Engine3D(scene, title='The Standford Rabbit', shading=shading)
    test.clear()
    test.rotate('y', 45)
    test.rotate('x', 45)
    test.render()
    test.mainloop()


if __name__ == '__main__':
    spawnrabbit()