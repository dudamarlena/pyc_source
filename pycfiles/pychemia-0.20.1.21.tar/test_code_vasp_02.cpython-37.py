# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/PyChemia/tests/test_code_vasp_02.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 2010 bytes
import pychemia
if pychemia.HAS_VTK:
    import vtk
    from vtk.util.colors import tomato
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetResolution(8)
    cylinderMapper = vtk.vtkPolyDataMapper()
    cylinderMapper.SetInputConnection(cylinder.GetOutputPort())
    cylinderActor = vtk.vtkActor()
    cylinderActor.SetMapper(cylinderMapper)
    cylinderActor.GetProperty().SetColor(tomato)
    cylinderActor.RotateX(30.0)
    cylinderActor.RotateY(-45.0)
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.AddActor(cylinderActor)
    ren.SetBackground(0.1, 0.2, 0.4)
    renWin.SetSize(200, 200)
    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()
    iren.Start()