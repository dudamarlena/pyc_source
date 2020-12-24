# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\__init__.py
# Compiled at: 2019-12-19 11:51:20
# Size of source mod 2**32: 12141 bytes
"""
LuxPy: a package for lighting and color science
===============================================

    * Author: K. A.G. Smet (ksmet1977 at gmail.com)
    * Version: 1.4.14
    * Date: Dec 19, 2019
    * License: GPLv3

    * DOI: https://doi.org/10.5281/zenodo.1298963
    * Cite: `Smet, K. A. G. (2019). Tutorial: The LuxPy Python Toolbox for Lighting and Color Science. LEUKOS, 1–23. DOI: 10.1080/15502724.2018.1518717 <https://www.tandfonline.com/doi/full/10.1080/15502724.2018.1518717>`_ 

License
-------
Copyright (C) <2017><Kevin A.G. Smet> (ksmet1977 at gmail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

LuxPy package structure
-----------------------
|       /utils
|               / helpers
|         helpers.py
|               /.math
|                       basics.py
|                       minimizebnd.py
|                       /.DEMO
|                               DEMO.py
|                               demo_opt.py
|                       /.vec3
|                               vec3.py                 
|       
|       /spectrum
|               cmf.py
|               spectral.py
|               spectral_databases.py
|       
|       /color
|               colortransformations.py
|               cct.py
|               /.cat
|                       chromaticadaptation.py  
|               /.cam
|                       colorappearancemodels.py
|                               cam_02_X.py
|                               cam15u.py
|                               sww16.py
|               colortf.py
|               /.deltaE
|                       colordifferences.py
|               /.cri
|                       colorrendition.py
|                       /utils
|                               DE_scalers.py
|                               helpers.py
|                               init_cri_defaults_database.py
|                               graphics.py
|                       /indices
|                               indices.py
|                                       cie_wrappers.py
|                                       ies_wrappers.py
|                                       cri2012.py
|                                       mcri.py
|                                       cqs.py
|                       /ies_tm30
|                               ies_tm30_metrics.py
|                               ies_tm30_graphics.py
|                       /.VFPX
|                               VF_PX_models.py (imported in .cri as .VFPX)
|                                       vectorshiftmodel.py
|                                       pixelshiftmodel.py
|               /utils
|                       plotters.py
|
|       /whiteness
|           smet_white_loci.py
|                       
|       /classes
|               SPD.py
|               CDATA.py
|               
|       /data
|               /cmfs
|               /spds
|               /rfls
|               /cctluts
|
|       /toolboxes
|               
|               /.photbiochem
|                       cie_tn003_2015.py
|                       /data
|                       
|               /.indvcmf
|                       individual_observer_cmf_model.py
|                       /data
|               
|               /.spdbuild
|                       spd_builder.py
|                       
|               /.hypspcsim
|                       hyperspectral_img_simulator.py
|
|       /.iolidfiles
|          io_lid_files.py
|       
|       /spectro
|          /jeti
|             jeti.py
|          /oceanoptics
|             oceanoptics.py
|
|       /rgb2spec
|           smits_mistuba.py

Imported core packages:
-----------------------
 * import os 
 * import warnings 
 * from collections import OrderedDict as odict 
 * from mpl_toolkits.mplot3d import Axes3D 
 * import colorsys 
 * import itertools 
 * import copy
 * import time
 * import tkinter
 * import ctypes
 * import platform
 
Imported 3e party dependencies (automatic install):
---------------------------------------------------
 * import numpy as np 
 * import pandas as pd 
 * import matplotlib.pyplot as plt 
 * import scipy as sp 
 * from scipy import interpolate 
 * from scipy.optimize import minimize 
 * from scipy.spatial import cKDTree 
 * from imageio import imsave
 
Imported 3e party dependencies (requiring manual install):
----------------------------------------------------------
To control Ocean Optics spectrometers with spectro toolbox:
 * import seabreeze (conda install -c poehlmann python-seabreeze)
 * pip install pyusb (for use with 'pyseabreeze' backend of python-seabreeze)

Global constants
----------------
The package uses several global constants that set the default state/behaviour
of the calculations. LuxPy 'global constants' start with '_' and are in an 
all _CAPITAL format. 

E.g.:
 * _PKG_PATH (absolute path to luxpy package)
 * _SEP (operating system operator)
 * _EPS = 7./3 - 4./3 -1 (machine epsilon)
 * _CIEOBS = '1931_2' (default CIE observer color matching function)
 * _CSPACE = 'Yuv' (default color space / chromaticity diagram)
 
DO NOT CHANGE THESE CONSTANTS!

"""
__VERSION__ = 'v1.4.14'
__AUTHOR__ = 'Kevin A.G. Smet'
__EMAIL__ = 'ksmet1977 at gmail.com'
__URL__ = 'github.com/ksmet1977/luxpy/'
__DATE__ = '19-Dec-2019'
__all__ = ['__VERSION__', '__AUTHOR__', '__EMAIL__', '__URL__', '__DATE__']
import os, warnings
from collections import OrderedDict as odict
from mpl_toolkits.mplot3d import Axes3D
import colorsys, itertools, copy, time, tkinter, ctypes, platform
__all__ += ['os', 'warnings', 'odict', 'Axes3D', 'colorsys', 'itertools', 'copy', 'time', 'tkinter', 'ctypes', 'platform']
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from imageio import imsave
__all__ += ['np', 'pd', 'plt', 'sp', 'interpolate', 'minimize', 'cKDTree', 'imsave']
np.set_printoptions(formatter={'float': lambda x: '{0:0.4e}'.format(x)})
np.seterr(over='ignore', under='ignore')
_PKG_PATH = os.path.dirname(__file__)
_SEP = os.sep
__all__ += ['_PKG_PATH', '_SEP']
_EPS = 2.220446049250313e-16
__all__ += ['_EPS']
_CIEOBS = '1931_2'
_CSPACE = 'Yuv'
__all__ += ['_CIEOBS', '_CSPACE']
from .utils.helpers import *
__all__ += utils.helpers.__all__
from .utils import math
__all__ += ['math']
from .spectrum.basics import *
__all__ += spectrum.basics.__all__
from .color.ctf.colortransforms import *
__all__ += color.ctf.colortransforms.__all__
from .color.cct.cct import *
__all__ += color.cct.cct.__all__
import color.cat as cat
__all__ += ['cat']
from .color.whiteness.smet_white_loci import *
__all__ += color.whiteness.smet_white_loci.__all__
import color.cam as cam
__all__ += ['cam']
from color.cam import _CAM_AXES, xyz_to_jabM_ciecam02, jabM_ciecam02_to_xyz, xyz_to_jabC_ciecam02, jabC_ciecam02_to_xyz, xyz_to_jabM_cam16, jabM_cam16_to_xyz, xyz_to_jabC_cam16, jabC_cam16_to_xyz, xyz_to_jab_cam02ucs, jab_cam02ucs_to_xyz, xyz_to_jab_cam02lcd, jab_cam02lcd_to_xyz, xyz_to_jab_cam02scd, jab_cam02scd_to_xyz, xyz_to_jab_cam16ucs, jab_cam16ucs_to_xyz, xyz_to_jab_cam16lcd, jab_cam16lcd_to_xyz, xyz_to_jab_cam16scd, jab_cam16scd_to_xyz, xyz_to_qabW_cam15u, qabW_cam15u_to_xyz, xyz_to_lab_cam_sww16, lab_cam_sww16_to_xyz, xyz_to_qabW_cam18sl, qabW_cam18sl_to_xyz, xyz_to_qabM_cam18sl, qabM_cam18sl_to_xyz, xyz_to_qabS_cam18sl, qabS_cam18sl_to_xyz
__all__ += ['_CAM_AXES',
 'xyz_to_jabM_ciecam02', 'jabM_ciecam02_to_xyz',
 'xyz_to_jabC_ciecam02', 'jabC_ciecam02_to_xyz',
 'xyz_to_jabM_cam16', 'jabM_cam16_to_xyz',
 'xyz_to_jabC_cam16', 'jabC_cam16_to_xyz',
 'xyz_to_jab_cam02ucs', 'jab_cam02ucs_to_xyz',
 'xyz_to_jab_cam02lcd', 'jab_cam02lcd_to_xyz',
 'xyz_to_jab_cam02scd', 'jab_cam02scd_to_xyz',
 'xyz_to_jab_cam16ucs', 'jab_cam16ucs_to_xyz',
 'xyz_to_jab_cam16lcd', 'jab_cam16lcd_to_xyz',
 'xyz_to_jab_cam16scd', 'jab_cam16scd_to_xyz',
 'xyz_to_qabW_cam15u', 'qabW_cam15u_to_xyz',
 'xyz_to_lab_cam_sww16', 'lab_cam_sww16_to_xyz',
 'xyz_to_qabW_cam18sl', 'qabW_cam18sl_to_xyz',
 'xyz_to_qabM_cam18sl', 'qabM_cam18sl_to_xyz',
 'xyz_to_qabS_cam18sl', 'qabS_cam18sl_to_xyz']
_CSPACE_AXES = {**_CSPACE_AXES, **_CAM_AXES}
from .color.ctf.colortf import *
__all__ += color.ctf.colortf.__all__
from .color.utils.plotters import *
__all__ += color.utils.plotters.__all__
from .color import deltaE
__all__ += ['deltaE']
import color.cri as cri
__all__ += ['cri']
import classes.SPD as SPD
from classes.CDATA import CDATA, XYZ, LAB
__all__ += ['SPD']
__all__ += ['CDATA', 'XYZ', 'LAB']
from .toolboxes import photbiochem
__all__ += ['photbiochem']
import toolboxes.indvcmf as indvcmf
__all__ += ['indvcmf']
from .toolboxes import spdbuild
__all__ += ['spdbuild']
import toolboxes.hypspcim as hypspcim
__all__ += ['hypspcim']
import toolboxes.iolidfiles as iolidfiles
__all__ += ['iolidfiles']
import toolboxes.spectro as spectro
__all__ += ['spectro']
from .toolboxes import rgb2spec
__all__ += ['rgb2spec']