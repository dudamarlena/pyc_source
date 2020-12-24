# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/vtkutils.py
# Compiled at: 2012-04-18 09:17:12
import vtk, numpy as np

def vtkmatrix4x4_to_array(vtkmat):
    numpy_array = np.zeros((4, 4), 'd')
    for i in range(0, 4):
        for j in range(0, 4):
            numpy_array[(i, j)] = vtkmat.GetElement(i, j)

    return numpy_array


def array_to_vtkmatrix4x4(numpy_array):
    mat = vtk.vtkMatrix4x4()
    for i in range(0, 4):
        for j in range(0, 4):
            mat.SetElement(i, j, numpy_array[(i, j)])

    return mat


def create_box_actor_around_marker(marker):
    boxSource = create_box_source(marker)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(boxSource.GetOutput())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(marker.get_color())
    actor.GetProperty().SetRepresentationToWireframe()
    actor.GetProperty().SetLineWidth(2.0)
    return actor


def create_box_source(marker):
    boxSource = vtk.vtkCubeSource()
    boxSource.SetBounds(marker.GetBounds())
    return boxSource