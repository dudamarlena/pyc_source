# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/__init__.py
# Compiled at: 2018-11-28 17:05:57
""" This module loads the entire VTK library into its namespace.  It
also allows one to use specific packages inside the vtk directory.."""
from __future__ import absolute_import
from .vtkCommonKit import *
from .vtkFiltersKit import *
from .vtkImagingKit import *
from .vtkRenderingKit import *
from .vtkIOKit import *
from .vtkOpenGLKit import *
from .vtkParallelKit import *
from .vtkWrappingKit import *
from .vtkInteractionKit import *
from .vtkViewsKit import *
from .vtkInfovisCore import *
from .vtkChartsCore import *
from .vtkDomainsChemistry import *
from .vtkFiltersFlowPaths import *
from .vtkFiltersHybrid import *
from .vtkImagingHybrid import *
from .vtkInfovisLayout import *
from .vtkGeovisCore import *
from .vtkRenderingGL2PSOpenGL2 import *
from .vtkIOExport import *
from .vtkIOExportOpenGL2 import *
from .vtkIOImport import *
from .vtkIOInfovis import *
from .vtkIOMINC import *
from .vtkIOTecplotTable import *
from .vtkViewsInfovis import *
__vtkTypeNameDict = {VTK_VOID: 'void', VTK_DOUBLE: 'double', 
   VTK_FLOAT: 'float', 
   VTK_LONG: 'long', 
   VTK_UNSIGNED_LONG: 'unsigned long', 
   VTK_INT: 'int', 
   VTK_UNSIGNED_INT: 'unsigned int', 
   VTK_SHORT: 'short', 
   VTK_UNSIGNED_SHORT: 'unsigned short', 
   VTK_CHAR: 'char', 
   VTK_UNSIGNED_CHAR: 'unsigned char', 
   VTK_SIGNED_CHAR: 'signed char', 
   VTK_LONG_LONG: 'long long', 
   VTK_UNSIGNED_LONG_LONG: 'unsigned long long', 
   VTK_ID_TYPE: 'vtkIdType', 
   VTK_BIT: 'bit'}

def vtkImageScalarTypeNameMacro(type):
    return __vtkTypeNameDict[type]


from .util.misc import calldata_type
from .util.vtkVariant import *