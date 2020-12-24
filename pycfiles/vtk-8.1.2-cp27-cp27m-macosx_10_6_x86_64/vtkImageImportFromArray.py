# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/util/vtkImageImportFromArray.py
# Compiled at: 2018-11-28 17:07:58
"""
vtkImageImportFromArray: a NumPy front-end to vtkImageImport

Load a python array into a vtk image.
To use this class, you must have NumPy installed (http://numpy.scipy.org/)

Methods:

  SetArray()  -- set the numpy array to load
  Update()    -- generate the output
  GetOutput() -- get the image as vtkImageData
  GetOutputPort() -- connect to VTK pipeline

Methods from vtkImageImport:
(if you don't set these, sensible defaults will be used)

  SetDataExtent()
  SetDataSpacing()
  SetDataOrigin()
"""
from vtk import vtkImageImport
from vtk import VTK_SIGNED_CHAR
from vtk import VTK_UNSIGNED_CHAR
from vtk import VTK_SHORT
from vtk import VTK_UNSIGNED_SHORT
from vtk import VTK_INT
from vtk import VTK_UNSIGNED_INT
from vtk import VTK_LONG
from vtk import VTK_UNSIGNED_LONG
from vtk import VTK_FLOAT
from vtk import VTK_DOUBLE

class vtkImageImportFromArray:

    def __init__(self):
        self.__import = vtkImageImport()
        self.__ConvertIntToUnsignedShort = False
        self.__Array = None
        return

    __typeDict = {'b': VTK_SIGNED_CHAR, 'B': VTK_UNSIGNED_CHAR, 
       'h': VTK_SHORT, 
       'H': VTK_UNSIGNED_SHORT, 
       'i': VTK_INT, 
       'I': VTK_UNSIGNED_INT, 
       'f': VTK_FLOAT, 
       'd': VTK_DOUBLE, 
       'F': VTK_FLOAT, 
       'D': VTK_DOUBLE}
    __sizeDict = {VTK_SIGNED_CHAR: 1, VTK_UNSIGNED_CHAR: 1, 
       VTK_SHORT: 2, 
       VTK_UNSIGNED_SHORT: 2, 
       VTK_INT: 4, 
       VTK_UNSIGNED_INT: 4, 
       VTK_FLOAT: 4, 
       VTK_DOUBLE: 8}

    def SetConvertIntToUnsignedShort(self, yesno):
        self.__ConvertIntToUnsignedShort = yesno

    def GetConvertIntToUnsignedShort(self):
        return self.__ConvertIntToUnsignedShort

    def ConvertIntToUnsignedShortOn(self):
        self.__ConvertIntToUnsignedShort = True

    def ConvertIntToUnsignedShortOff(self):
        self.__ConvertIntToUnsignedShort = False

    def Update(self):
        self.__import.Update()

    def GetOutputPort(self):
        return self.__import.GetOutputPort()

    def GetOutput(self):
        return self.__import.GetOutput()

    def SetArray(self, imArray):
        self.__Array = imArray
        numComponents = 1
        dim = imArray.shape
        if len(dim) == 0:
            dim = (1, 1, 1)
        elif len(dim) == 1:
            dim = (
             1, 1, dim[0])
        elif len(dim) == 2:
            dim = (
             1, dim[0], dim[1])
        elif len(dim) == 4:
            numComponents = dim[3]
            dim = (dim[0], dim[1], dim[2])
        typecode = imArray.dtype.char
        ar_type = self.__typeDict[typecode]
        complexComponents = 1
        if typecode == 'F' or typecode == 'D':
            numComponents = numComponents * 2
            complexComponents = 2
        if self.__ConvertIntToUnsignedShort and typecode == 'i':
            imArray = imArray.astype('h')
            ar_type = VTK_UNSIGNED_SHORT
        size = len(imArray.flat) * self.__sizeDict[ar_type] * complexComponents
        self.__import.CopyImportVoidPointer(imArray, size)
        self.__import.SetDataScalarType(ar_type)
        self.__import.SetNumberOfScalarComponents(numComponents)
        extent = self.__import.GetDataExtent()
        self.__import.SetDataExtent(extent[0], extent[0] + dim[2] - 1, extent[2], extent[2] + dim[1] - 1, extent[4], extent[4] + dim[0] - 1)
        self.__import.SetWholeExtent(extent[0], extent[0] + dim[2] - 1, extent[2], extent[2] + dim[1] - 1, extent[4], extent[4] + dim[0] - 1)

    def GetArray(self):
        return self.__Array

    def SetDataExtent(self, extent):
        self.__import.SetDataExtent(extent)

    def GetDataExtent(self):
        return self.__import.GetDataExtent()

    def SetDataSpacing(self, spacing):
        self.__import.SetDataSpacing(spacing)

    def GetDataSpacing(self):
        return self.__import.GetDataSpacing()

    def SetDataOrigin(self, origin):
        self.__import.SetDataOrigin(origin)

    def GetDataOrigin(self):
        return self.__import.GetDataOrigin()