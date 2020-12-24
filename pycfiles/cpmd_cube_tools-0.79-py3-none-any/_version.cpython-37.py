# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/lv_we/data/codes/tools_lib/cpmd_cube_tools/release/cpmd_cube_tools/_version.py
# Compiled at: 2020-04-23 20:46:27
# Size of source mod 2**32: 915 bytes
"""
-----------
CPMD_Cube_Tools
-----------

Author: Wade LYU
email: lyuwade@gmail.com

A python library and tool to read in and manipulate Gaussian and CPMD cube files. This code allows you to:
    Read and write Gaussian/CPMD cube files
    Perform VDD charge analysis

Acknowledgment: This code is partially developed based on the Cube-Toolz @ https://github.com/funkymunkycool/Cube-Toolz/blob/master/cube_tools.py

Version      Date              Coder          Changes
=======   ==========        ===========       =======
0.6       05/08/2019        Wade Lyu          Corrected the coordinates of cube file by external geometry information, and formated cube output
0.7       02/10/2019        Wade Lyu          Implemention of Voronoi deformation density (VDD) method for charge analysis
0.79      24/04/2020        Wade Lyu          Cleaned-up and Reformated the core part of the package

"""
version = 0.79