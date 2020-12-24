# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\utils\__init__.py
# Compiled at: 2017-05-31 20:05:28
# Size of source mod 2**32: 813 bytes
""" Package visvis.utils

This package contains a few modules and packages that are stand-alone
and maybe useful outside visvis. Some utilities are used inside visvis
(such as ssdf), others extend the functionality of visvis or have some
relation to visualization.

The intended way to import utilities is: "from visvis.utils import utilname".

The currrent utilities are:

  * ssdf - simple structured data format.
  * pypoints - Representnig points, pointsets, anisotropic arrays and quaternions.
  * graph - Representing points/nodes that are connected by edges.
  * cropper - small app based on visvis controls to crop 3D data

"""