# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/vtkNifti.py
# Compiled at: 2012-04-18 09:16:22
from nibabel import load
import numpy as np, vtk
from shared import shared
from vtkutils import array_to_vtkmatrix4x4

class vtkNiftiImageReader(object):
    __defaultFilePattern = ''

    def __init__(self):
        self.__vtkimport = vtk.vtkImageImport()
        self.__vtkimport.SetDataScalarTypeToFloat()
        self.__vtkimport.SetNumberOfScalarComponents(1)
        self.__filePattern = self.__defaultFilePattern
        self.__data = None
        self._irs = vtk.vtkImageReslice()
        return

    def SetFileName(self, filename):
        self.__filename = filename

    def Update(self):
        if shared.debug:
            print 'Loading ', self.__filename
        self.__nim = load(self.__filename)
        if shared.debug:
            print self.__nim
        self.__data = self.__nim.get_data().astype('f').swapaxes(0, 2)
        self.__vtkimport.SetWholeExtent(0, self.__data.shape[2] - 1, 0, self.__data.shape[1] - 1, 0, self.__data.shape[0] - 1)
        self.__vtkimport.SetDataExtentToWholeExtent()
        voxdim = self.__nim.get_header()['pixdim'][:3].copy()
        self.__data_string = self.__data.tostring()
        if shared.debug:
            print voxdim
        self.__vtkimport.SetDataSpacing((1.0, 1.0, 1.0))
        self.__vtkimport.CopyImportVoidPointer(self.__data_string, len(self.__data_string))
        self.__vtkimport.UpdateWholeExtent()
        imgData1 = self.__vtkimport.GetOutput()
        imgData1.SetExtent(self.__vtkimport.GetDataExtent())
        imgData1.SetOrigin((0, 0, 0))
        imgData1.SetSpacing(1.0, 1.0, 1.0)
        self._irs.SetInput(imgData1)
        self._irs.SetInterpolationModeToCubic()
        affine = array_to_vtkmatrix4x4(self.__nim.get_affine())
        if shared.debug:
            print self._irs.GetResliceAxesOrigin()
        self._irs.SetResliceAxes(affine)
        if shared.debug:
            print self._irs.GetResliceAxesOrigin()
        m2t = vtk.vtkMatrixToLinearTransform()
        m2t.SetInput(affine.Invert())
        self._irs.TransformInputSamplingOff()
        self._irs.SetResliceTransform(m2t.MakeTransform())
        if shared.debug:
            print voxdim, self._irs.GetOutputSpacing()
        self._irs.SetOutputSpacing(abs(voxdim))
        if shared.debug:
            print self._irs.GetOutputSpacing()
        self._irs.AutoCropOutputOn()
        self._irs.Update()

    def GetWidth(self):
        return self._irs.GetOutput().GetBounds()[0:2]

    def GetHeight(self):
        return self._irs.GetOutput().GetBounds()[2:4]

    def GetDepth(self):
        return self._irs.GetOutput().GetBouds()[4:]

    def GetDataSpacing(self):
        if shared.debug:
            print self.__spacing, '*******************'
        return self._irs.GetOutput().GetSpacing()

    def GetOutput(self):
        return self._irs.GetOutput()

    def GetFilename(self):
        if shared.debug:
            print self.__filename
        return self.__filename

    def GetDataExtent(self):
        return self._irs.GetOutput().GetDataExtent()

    def GetBounds(self):
        return self._irs.GetOutput().GetBounds()

    def GetQForm(self):
        return self.__nim.get_affine()

    @property
    def nifti_voxdim(self):
        return self.__nim.get_header()['pixdim'][:3]

    @property
    def shape(self):
        return self.__nim.shape

    @property
    def min(self):
        if self.__data != None:
            return self.__data.min()
        else:
            return

    @property
    def max(self):
        if self.__data != None:
            return self.__data.max()
        else:
            return

    @property
    def median(self):
        d = self.__data
        if d != None:
            return np.median(d[(d != 0)])
        else:
            return


if __name__ == '__main__':
    reader = vtkNiftiImageReader()
    reader.SetFileName('/home/thorsten/Dokumente/pylocator-examples/Can7/mri/post2std_brain.nii.gz')
    reader.Update()
    print reader._irs
    print reader.GetOutput()