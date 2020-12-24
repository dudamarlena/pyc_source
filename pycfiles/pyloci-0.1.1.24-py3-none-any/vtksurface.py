# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/vtksurface.py
# Compiled at: 2012-04-18 09:16:44
import vtk
from events import EventHandler
from vtkutils import vtkmatrix4x4_to_array, array_to_vtkmatrix4x4

class VTKSurface(vtk.vtkActor):
    """
    CLASS: VTKSurface
    DESCR: Handles a .vtk structured points file.
    """

    def set_matrix(self, registration_mat):
        print 'VTKSurface.set_matrix(', registration_mat, ')!!'
        mat = array_to_vtkmatrix4x4(registration_mat)
        mat.Modified()
        mat2xform = vtk.vtkMatrixToLinearTransform()
        mat2xform.SetInput(mat)
        print 'calling SetUserTransform(', mat2xform, ')'
        self.SetUserTransform(mat2xform)
        self.Modified()
        self.renderer.Render()

    def __init__(self, filename, renderer):
        self.renderer = renderer
        reader = vtk.vtkStructuredPointsReader()
        reader.SetFileName(filename)
        imagedata = reader.GetOutput()
        cf = vtk.vtkContourFilter()
        cf.SetInput(imagedata)
        cf.SetValue(0, 1)
        deci = vtk.vtkDecimatePro()
        deci.SetInput(cf.GetOutput())
        deci.SetTargetReduction(0.1)
        deci.PreserveTopologyOn()
        smoother = vtk.vtkSmoothPolyDataFilter()
        smoother.SetInput(deci.GetOutput())
        smoother.SetNumberOfIterations(100)
        normals = vtk.vtkPolyDataNormals()
        normals.SetInput(smoother.GetOutput())
        normals.FlipNormalsOn()
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0, 0)
        lut.SetSaturationRange(0, 0)
        lut.SetValueRange(0.2, 0.55)
        contourMapper = vtk.vtkPolyDataMapper()
        contourMapper.SetInput(normals.GetOutput())
        contourMapper.SetLookupTable(lut)
        self.contours = vtk.vtkActor()
        self.contours.SetMapper(contourMapper)
        self.contours.GetProperty().SetRepresentationToSurface()
        self.contours.GetProperty().SetInterpolationToGouraud()
        self.contours.GetProperty().SetOpacity(1.0)
        self.contours.GetProperty().SetAmbient(0.1)
        self.contours.GetProperty().SetDiffuse(0.1)
        self.contours.GetProperty().SetSpecular(0.1)
        self.contours.GetProperty().SetSpecularPower(0.1)
        renderer.AddActor(self.contours)
        print 'PlaneWidgetsXYZ.set_image_data: setting EventHandler.set_vtkactor(self.contours)!'
        EventHandler().set_vtkactor(self.contours)