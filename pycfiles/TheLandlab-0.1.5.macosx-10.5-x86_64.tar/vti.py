# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/io/vtk/vti.py
# Compiled at: 2014-09-23 12:37:24
from landlab.io.vtk.writer import VtkWriter
from landlab.io.vtk.vtktypes import VtkUniformRectilinear
from landlab.io.vtk.vtkxml import VtkRootElement, VtkGridElement, VtkPieceElement, VtkCoordinatesElement, VtkPointDataElement, VtkCellDataElement, VtkExtent

class VtkUniformRectilinearWriter(VtkWriter):
    _vtk_grid_type = VtkUniformRectilinear

    def construct_field_elements(self, field):
        extent = VtkExtent(field.shape[::-1])
        origin = VtkOrigin(field.origin[::-1], field.spacing[::-1])
        spacing = VtkSpacing(field.spacing[::-1])
        element = {'VTKFile': VtkRootElement(VtkUniformRectilinear), 
           'Grid': VtkGridElement(VtkUniformRectilinear, WholeExtent=extent, Origin=origin, Spacing=spacing), 
           'Piece': VtkPieceElement(Extent=extent), 
           'PointData': VtkPointDataElement(field.at_node, append=self.data, encoding=self.encoding), 
           'CellData': VtkCellDataElement(field.at_cell, append=data, encoding=encoding)}
        return element