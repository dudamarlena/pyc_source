# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/lv_we/data/codes/tools_lib/cpmd_cube_tools/release/cpmd_cube_tools/api.py
# Compiled at: 2020-04-23 10:52:40
# Size of source mod 2**32: 2025 bytes
from cpmd_cube_tools.core import *

def add_cubes(files):
    cubes = [cube(fin) for fin in files]
    print('====== Adding cube files ======')
    cube_out = copy.deepcopy(cubes[0])
    for ctmp in cubes[1:]:
        cube_out.data += ctmp.data

    print('====== Writing output cube as diff.cube ======')
    cube_out.write_cube('diff.cube')
    return cube_out


def align2cube(cube1, cube2):
    """
    Align 2ed cube file to the first cube file
    """
    delt = np.array(cube1.atomsXYZ[0]) - np.array(cube2.atomsXYZ[0])
    print('delt: ', delt)
    cube2.translate_cube(delt)


def diff_cubes(files):
    cubes = [cube(fin) for fin in files]
    print('====== Subtracting cube files ======')
    cube_out = copy.deepcopy(cubes[0])
    for i in range(1, len(files)):
        ctmp = cubes[i]
        align2cube(cubes[0], ctmp)
        ctmp.write_cube(files[i] + '_align2_' + files[0])
        cube_out.data -= ctmp.data

    print('====== Writing output cube as diff.cube ======')
    cube_out.write_cube('diff.cube')
    return cube_out


def translate_cubes(files, tVector):
    cubes = [cube(fin) for fin in files]
    print('====== Squaring cube files ======')
    [ctmp.translate_cube(tVector) for ctmp in cubes]
    print('====== Writing output cubes as translateN.cube ======')
    if len(cubes) == 1:
        cubes[0].write_cube('translate.cube')
    else:
        for ind, cout in enumerate(cubes):
            cout.write_cube('translate%d.cube' % ind)


def correct_cube(files, geom):
    cubes = cube(files)
    print('===== Correct CUBE coordinates=====')
    cubes.correct_cube(geom)
    print('====== Writing output cubes as ' + files.split('.')[0] + '_corrected.cube ======')
    cubes.write_cube(files.split('.')[0] + '_corrected.cube')


def cube2vdd(files, geom, inpf):
    cubes = cube(files)
    print('==== performing vdd analysis =====')
    cubes.cube2vdd(geom, inpf)