# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/core/consts.py
# Compiled at: 2020-04-24 23:10:11
# Size of source mod 2**32: 1496 bytes
"""
Module that contains constant definitions for tpDcc
"""
from __future__ import print_function, division, absolute_import
from tpDcc.libs.python import python
if python.is_python2():
    from aenum import Enum
else:
    from enum import Enum
PROJECTS_NAME = 'project.json'
CODE_FOLDER = '__code__'
DATA_FOLDER = '__data__'
BACKUP_FOLDER = '__backup__'
VERSIONS_FOLDER = '__versions__'
MANIFEST_FILE = 'manifest.data'
DATA_FILE = 'data.json'
DELETE_PROJECT_TOOLTIP = 'Delete selected project'
OPEN_PROJECT_IN_EXPLORER_TOOLTIP = 'Open Project Folder in Explorer'
SET_PROJECT_IMAGE_TOOLTIP = 'Set the Image used for the Project'

class PointerTypes(Enum):
    Shape = 0
    Transform = 1
    Pointer = 2


class ObjectTypes(Enum):
    Generic = 0
    Sphere = 1
    Box = 2
    Cylinder = 3
    Capsule = 4
    Geometry = 5
    Model = 6
    PolyMesh = 7
    NurbsSurface = 8
    Curve = 9
    Light = 10
    Camera = 11
    Group = 12
    Null = 13
    Bone = 14
    Particle = 15
    Network = 16
    Circle = 17
    Biped = 18


class UnitSystem(Enum):
    Inches = 0
    Feet = 1
    Millimeters = 2
    Centimeters = 3
    Meters = 4
    Kilometers = 5
    Yards = 6
    Miles = 7


class MaterialAttributeTypes(Enum):
    Int = 0
    Float = 1
    String = 2
    Path = 3
    Color = 4
    Bool = 5


class MaterialTypes(Enum):
    Standard = 0