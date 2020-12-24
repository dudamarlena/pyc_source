# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/io.py
# Compiled at: 2019-10-29 11:22:24
# Size of source mod 2**32: 541 bytes
"""Input and output functionality."""
import iris
__all__ = ('load_multidir', )

def load_multidir(path_mask, labels, label_name='run'):
    """Load cubelists from multiple directories and merge."""
    joint_cl = iris.cube.CubeList()
    for label in labels:
        cl = iris.load(str(path_mask).format(label))
        for cube in cl:
            cube.attributes['um_version'] = ''
            cube.add_aux_coord(iris.coords.AuxCoord([label], long_name=label_name))
            joint_cl.append(cube)
        else:
            return joint_cl.merge()