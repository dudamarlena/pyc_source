# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/regrid/flowgrid/SUTRA.py
# Compiled at: 2018-10-28 11:56:32
# Size of source mod 2**32: 4675 bytes
import regrid.flowgrid.FlowGrid as FlowGrid
import numpy as np, vtk

class SUTRA(FlowGrid):
    __doc__ = ' SUTRA is a USGS flow modelling code.  \n    '

    def __init__(self):
        super(SUTRA, self).__init__()
        nx, ny, nz = (0, 0, 0)

    def loadPointsOnly(self, fname):
        pass

    def loadNodes(self, fname, nx, ny, nz):
        """ Reads in the points of the grid, ususally in a file called nodewise
            fname = nodes file 
            nx = number of cells in the easting(x) direction 
            ny = number of cells in the northing (y) direction 
            nz = number of cells in depth, positive up 
            This method results in the generation of a VtkStructuredGrid
        """
        self.nx = nx
        self.ny = ny
        self.nz = nz
        X = np.loadtxt(fname, comments='#')
        self.points = np.reshape(np.array((X[:, 2], X[:, 3], X[:, 4])).T, (nx, ny, nz, 3))
        self.sGrid = vtk.vtkStructuredGrid()
        self.sGrid.SetDimensions(124, 88, 4)
        vtk_points = vtk.vtkPoints()
        for iz in range(nz):
            for iy in range(ny):
                for ix in range(nx):
                    vtk_points.InsertNextPoint(self.points[(ix, iy, iz)][0], self.points[(ix, iy, iz)][1], self.points[(ix, iy, iz)][2])

        else:
            self.sGrid.SetPoints(vtk_points)

    def loadNodesConnections(self, nodes, connections):
        """ In contrast to the above method, the points and connections can be loaded instead. For non-regular grids 
            this is necessary. This method results in the generation of a vtkUnstructuredGrid
            nodes = node file, often called nodewise
            connections = element connections, often called incident
        """
        X = np.loadtxt(nodes, comments='#')
        points = np.array((X[:, 2], X[:, 3], 10.0 * X[:, 4])).T


def loadSUTRA():
    points = np.array((X[:, 2], X[:, 3], 10.0 * X[:, 4])).T
    nnodes = np.shape(points)[0]
    uGrid = vtk.vtkUnstructuredGrid()
    sGrid = vtk.vtkStructuredGrid()
    vtk_points = vtk.vtkPoints()
    vtk_spoints = vtk.vtkPoints()
    for point in range(np.shape(points)[0]):
        vtk_points.InsertNextPoint(points[(point, 0)], points[(point, 1)], points[(point, 2)])
    else:
        uGrid.SetPoints(vtk_points)
        sGrid.SetPoints(vtk_points)
        sGrid.SetDimensions(124, 88, 4)
        C = np.loadtxt('incident', comments='#', skiprows=2, dtype=int)
        for line in range(np.shape(C)[0]):
            idList = vtk.vtkIdList()
            for node in C[line, :][1:]:
                idList.InsertNextId(node - 1)
            else:
                uGrid.InsertNextCell(vtk.VTK_HEXAHEDRON, idList)

        else:
            k = np.loadtxt('element_Sperm', comments='#')
            kx = vtk.vtkDoubleArray()
            kx.SetName('$\\kappa_x$')
            ky = vtk.vtkDoubleArray()
            ky.SetName('$\\kappa_y$')
            kz = vtk.vtkDoubleArray()
            kz.SetName('$\\kappa_z$')
            for ik, K in enumerate(k):
                kx.InsertNextTuple1(K[2])
                ky.InsertNextTuple1(K[3])
                kz.InsertNextTuple1(K[4])
            else:
                uGrid.GetCellData().AddArray(kx)
                uGrid.GetCellData().AddArray(ky)
                uGrid.GetCellData().AddArray(kz)
                phi = np.loadtxt('node_Spor')
                vphi = vtk.vtkDoubleArray()
                vphi.SetName('$\\phi$')
                for ik, K in enumerate(phi):
                    vphi.InsertNextTuple1(K[5])
                else:
                    uGrid.GetPointData().AddArray(vphi)
                    P = np.loadtxt('../InjModel7/Inj7.nod', comments='#')
                    vP = vtk.vtkDoubleArray()
                    vP.SetName('$P$')
                    for ik in range(nnodes):
                        vP.InsertNextTuple1(P[(2 * nnodes + ik, 3)])
                    else:
                        uGrid.GetPointData().AddArray(vP)
                        uWrite = vtk.vtkXMLUnstructuredGridWriter()
                        uWrite.SetInputData(uGrid)
                        uWrite.SetFileName('sutra.vtu')
                        uWrite.Write()
                        sWrite = vtk.vtkXMLStructuredGridWriter()
                        sWrite.SetInputData(sGrid)
                        sWrite.SetFileName('sutra.vts')
                        sWrite.Write()


if __name__ == '__main__':
    Mod = SUTRA()
    Mod.loadPoints('nodewise', 124, 88, 4)
    Mod.exportVTK('test.vts')