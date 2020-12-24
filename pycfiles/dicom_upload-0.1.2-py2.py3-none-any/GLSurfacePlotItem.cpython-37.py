# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLSurfacePlotItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5204 bytes
from OpenGL.GL import *
from .GLMeshItem import GLMeshItem
from ..MeshData import MeshData
from ...Qt import QtGui
import numpy as np
__all__ = [
 'GLSurfacePlotItem']

class GLSurfacePlotItem(GLMeshItem):
    """GLSurfacePlotItem"""

    def __init__(self, x=None, y=None, z=None, colors=None, **kwds):
        """
        The x, y, z, and colors arguments are passed to setData().
        All other keyword arguments are passed to GLMeshItem.__init__().
        """
        self._x = None
        self._y = None
        self._z = None
        self._color = None
        self._vertexes = None
        self._meshdata = MeshData()
        (GLMeshItem.__init__)(self, meshdata=self._meshdata, **kwds)
        self.setData(x, y, z, colors)

    def setData(self, x=None, y=None, z=None, colors=None):
        """
        Update the data in this surface plot. 
        
        ==============  =====================================================================
        **Arguments:**
        x,y             1D arrays of values specifying the x,y positions of vertexes in the
                        grid. If these are omitted, then the values will be assumed to be
                        integers.
        z               2D array of height values for each grid vertex.
        colors          (width, height, 4) array of vertex colors.
        ==============  =====================================================================
        
        All arguments are optional.
        
        Note that if vertex positions are updated, the normal vectors for each triangle must 
        be recomputed. This is somewhat expensive if the surface was initialized with smooth=False
        and very expensive if smooth=True. For faster performance, initialize with 
        computeNormals=False and use per-vertex colors or a normal-independent shader program.
        """
        if x is not None:
            if not self._x is None:
                if len(x) != len(self._x):
                    self._vertexes = None
                self._x = x
            else:
                if y is not None:
                    if self._y is None or len(y) != len(self._y):
                        self._vertexes = None
                    self._y = y
                if z is not None:
                    if self._x is not None:
                        if z.shape[0] != len(self._x):
                            raise Exception('Z values must have shape (len(x), len(y))')
                    if self._y is not None:
                        if z.shape[1] != len(self._y):
                            raise Exception('Z values must have shape (len(x), len(y))')
                    self._z = z
                    if self._vertexes is not None:
                        if self._z.shape != self._vertexes.shape[:2]:
                            self._vertexes = None
            if colors is not None:
                self._colors = colors
                self._meshdata.setVertexColors(colors)
            if self._z is None:
                return
            updateMesh = False
            newVertexes = False
            if self._vertexes is None:
                newVertexes = True
                self._vertexes = np.empty((self._z.shape[0], self._z.shape[1], 3), dtype=float)
                self.generateFaces()
                self._meshdata.setFaces(self._faces)
                updateMesh = True
        else:
            if not newVertexes:
                if x is not None:
                    if x is None:
                        if self._x is None:
                            x = np.arange(self._z.shape[0])
                        else:
                            x = self._x
                    self._vertexes[:, :, 0] = x.reshape(len(x), 1)
                    updateMesh = True
                if newVertexes or y is not None:
                    if y is None:
                        if self._y is None:
                            y = np.arange(self._z.shape[1])
            else:
                y = self._y
            self._vertexes[:, :, 1] = y.reshape(1, len(y))
            updateMesh = True
        if newVertexes or z is not None:
            self._vertexes[(Ellipsis, 2)] = self._z
            updateMesh = True
        if updateMesh:
            self._meshdata.setVertexes(self._vertexes.reshape(self._vertexes.shape[0] * self._vertexes.shape[1], 3))
            self.meshDataChanged()

    def generateFaces(self):
        cols = self._z.shape[1] - 1
        rows = self._z.shape[0] - 1
        faces = np.empty((cols * rows * 2, 3), dtype=(np.uint))
        rowtemplate1 = np.arange(cols).reshape(cols, 1) + np.array([[0, 1, cols + 1]])
        rowtemplate2 = np.arange(cols).reshape(cols, 1) + np.array([[cols + 1, 1, cols + 2]])
        for row in range(rows):
            start = row * cols * 2
            faces[start:start + cols] = rowtemplate1 + row * (cols + 1)
            faces[start + cols:start + cols * 2] = rowtemplate2 + row * (cols + 1)

        self._faces = faces