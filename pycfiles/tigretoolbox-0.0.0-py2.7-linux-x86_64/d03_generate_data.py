# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Demos/d03_generate_data.py
# Compiled at: 2017-06-20 08:49:49
import os, sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path:
    sys.path.append(rootDir)
import numpy as np, Demos.geometry as geometry, Test_data.data_loader as data_loader, scipy.io, Utilities.plotting_utils as plotter
from _Ax import Ax
TIGRE_parameters = geometry.TIGREParameters(high_quality=False)
head = data_loader.load_head_phantom(number_of_voxels=TIGRE_parameters.nVoxel)
angles = np.linspace(0, 2 * np.pi, 20, dtype=np.float32)
projections = Ax(head, TIGRE_parameters, angles, 'interpolated')
plotter.plot_projections(projections)