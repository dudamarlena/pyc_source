# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/__init__.py
# Compiled at: 2020-04-22 18:20:04
# Size of source mod 2**32: 1348 bytes
"""
Tiny 3D Engine structure :
==========================

Read the parts of the engine in the following order

geo_loader:
-----------

This module loads ensight ASCII geometries.
These files a the typical material gieven to tiny 3D engine.

scene3d:
--------

Scene3D is an object gathering different parts 
of differenct coloss and connectivity.
These parts exists in a 3D cartesian world, 
with absolute coordinates.

engine:
-------

The engine itself, load a **Scene3D** object.
The scene is given to a WiewField objets, 
where the geoetric transformations will occur.
The engine also instatiate a **screen** object,
where all the Graphical actions are done.

viewfield:
----------

The **ViewField** object load the coordinates of the scene once.
However, it actually stores the coordianates with respect to
the user field of vision. 
All the interactions will alter the coordinates of the view fields, 
by rotation, translation or scaling.

Screen:
-------

The screen object is the canevas where everything is drawn.
** All the graphical toolkit, Here the Tkinter canvas, is limited to this object**

"""
from .scene3d import *
from .part3d import *
from .engine import *
from .viewfield import *
from .screen import *
from .geo_loader import *
from .ply_loader import *
from .examples.geoload import *
from .examples.benchmark import *