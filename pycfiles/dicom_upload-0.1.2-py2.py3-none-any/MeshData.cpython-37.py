# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/MeshData.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 22155 bytes
from ..Qt import QtGui
from .. import functions as fn
import numpy as np

class MeshData(object):
    """MeshData"""

    def __init__(self, vertexes=None, faces=None, edges=None, vertexColors=None, faceColors=None):
        """
        ==============  =====================================================
        **Arguments:**
        vertexes        (Nv, 3) array of vertex coordinates.
                        If faces is not specified, then this will instead be
                        interpreted as (Nf, 3, 3) array of coordinates.
        faces           (Nf, 3) array of indexes into the vertex array.
        edges           [not available yet]
        vertexColors    (Nv, 4) array of vertex colors.
                        If faces is not specified, then this will instead be
                        interpreted as (Nf, 3, 4) array of colors.
        faceColors      (Nf, 4) array of face colors.
        ==============  =====================================================
        
        All arguments are optional.
        """
        self._vertexes = None
        self._vertexesIndexedByFaces = None
        self._vertexesIndexedByEdges = None
        self._faces = None
        self._edges = None
        self._vertexFaces = None
        self._vertexEdges = None
        self._vertexNormals = None
        self._vertexNormalsIndexedByFaces = None
        self._vertexColors = None
        self._vertexColorsIndexedByFaces = None
        self._vertexColorsIndexedByEdges = None
        self._faceNormals = None
        self._faceNormalsIndexedByFaces = None
        self._faceColors = None
        self._faceColorsIndexedByFaces = None
        self._faceColorsIndexedByEdges = None
        self._edgeColors = None
        self._edgeColorsIndexedByEdges = None
        if vertexes is not None:
            if faces is None:
                self.setVertexes(vertexes, indexed='faces')
                if vertexColors is not None:
                    self.setVertexColors(vertexColors, indexed='faces')
                if faceColors is not None:
                    self.setFaceColors(faceColors, indexed='faces')
            else:
                self.setVertexes(vertexes)
                self.setFaces(faces)
                if vertexColors is not None:
                    self.setVertexColors(vertexColors)
                if faceColors is not None:
                    self.setFaceColors(faceColors)

    def faces(self):
        """Return an array (Nf, 3) of vertex indexes, three per triangular face in the mesh.
        
        If faces have not been computed for this mesh, the function returns None.
        """
        return self._faces

    def edges(self):
        """Return an array (Nf, 3) of vertex indexes, two per edge in the mesh."""
        if self._edges is None:
            self._computeEdges()
        return self._edges

    def setFaces(self, faces):
        """Set the (Nf, 3) array of faces. Each rown in the array contains
        three indexes into the vertex array, specifying the three corners 
        of a triangular face."""
        self._faces = faces
        self._edges = None
        self._vertexFaces = None
        self._vertexesIndexedByFaces = None
        self.resetNormals()
        self._vertexColorsIndexedByFaces = None
        self._faceColorsIndexedByFaces = None

    def vertexes(self, indexed=None):
        """Return an array (N,3) of the positions of vertexes in the mesh. 
        By default, each unique vertex appears only once in the array.
        If indexed is 'faces', then the array will instead contain three vertexes
        per face in the mesh (and a single vertex may appear more than once in the array)."""
        if indexed is None:
            if self._vertexes is None:
                if self._vertexesIndexedByFaces is not None:
                    self._computeUnindexedVertexes()
            return self._vertexes
        if indexed == 'faces':
            if self._vertexesIndexedByFaces is None:
                if self._vertexes is not None:
                    self._vertexesIndexedByFaces = self._vertexes[self.faces()]
            return self._vertexesIndexedByFaces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def setVertexes(self, verts=None, indexed=None, resetNormals=True):
        """
        Set the array (Nv, 3) of vertex coordinates.
        If indexed=='faces', then the data must have shape (Nf, 3, 3) and is
        assumed to be already indexed as a list of faces.
        This will cause any pre-existing normal vectors to be cleared
        unless resetNormals=False.
        """
        if indexed is None:
            if verts is not None:
                self._vertexes = verts
            self._vertexesIndexedByFaces = None
        elif indexed == 'faces':
            self._vertexes = None
            if verts is not None:
                self._vertexesIndexedByFaces = verts
        else:
            raise Exception("Invalid indexing mode. Accepts: None, 'faces'")
        if resetNormals:
            self.resetNormals()

    def resetNormals(self):
        self._vertexNormals = None
        self._vertexNormalsIndexedByFaces = None
        self._faceNormals = None
        self._faceNormalsIndexedByFaces = None

    def hasFaceIndexedData(self):
        """Return True if this object already has vertex positions indexed by face"""
        return self._vertexesIndexedByFaces is not None

    def hasEdgeIndexedData(self):
        return self._vertexesIndexedByEdges is not None

    def hasVertexColor(self):
        """Return True if this data set has vertex color information"""
        for v in (self._vertexColors, self._vertexColorsIndexedByFaces, self._vertexColorsIndexedByEdges):
            if v is not None:
                return True

        return False

    def hasFaceColor(self):
        """Return True if this data set has face color information"""
        for v in (self._faceColors, self._faceColorsIndexedByFaces, self._faceColorsIndexedByEdges):
            if v is not None:
                return True

        return False

    def faceNormals(self, indexed=None):
        """
        Return an array (Nf, 3) of normal vectors for each face.
        If indexed='faces', then instead return an indexed array
        (Nf, 3, 3)  (this is just the same array with each vector
        copied three times).
        """
        if self._faceNormals is None:
            v = self.vertexes(indexed='faces')
            self._faceNormals = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
        if indexed is None:
            return self._faceNormals
        if indexed == 'faces':
            if self._faceNormalsIndexedByFaces is None:
                norms = np.empty((self._faceNormals.shape[0], 3, 3))
                norms[:] = self._faceNormals[:, np.newaxis, :]
                self._faceNormalsIndexedByFaces = norms
            return self._faceNormalsIndexedByFaces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def vertexNormals(self, indexed=None):
        """
        Return an array of normal vectors.
        By default, the array will be (N, 3) with one entry per unique vertex in the mesh.
        If indexed is 'faces', then the array will contain three normal vectors per face
        (and some vertexes may be repeated).
        """
        if self._vertexNormals is None:
            faceNorms = self.faceNormals()
            vertFaces = self.vertexFaces()
            self._vertexNormals = np.empty((self._vertexes.shape), dtype=float)
            for vindex in xrange(self._vertexes.shape[0]):
                faces = vertFaces[vindex]
                if len(faces) == 0:
                    self._vertexNormals[vindex] = (0, 0, 0)
                    continue
                norms = faceNorms[faces]
                norm = norms.sum(axis=0)
                norm /= (norm ** 2).sum() ** 0.5
                self._vertexNormals[vindex] = norm

        if indexed is None:
            return self._vertexNormals
        if indexed == 'faces':
            return self._vertexNormals[self.faces()]
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def vertexColors(self, indexed=None):
        """
        Return an array (Nv, 4) of vertex colors.
        If indexed=='faces', then instead return an indexed array
        (Nf, 3, 4). 
        """
        if indexed is None:
            return self._vertexColors
        if indexed == 'faces':
            if self._vertexColorsIndexedByFaces is None:
                self._vertexColorsIndexedByFaces = self._vertexColors[self.faces()]
            return self._vertexColorsIndexedByFaces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def setVertexColors(self, colors, indexed=None):
        """
        Set the vertex color array (Nv, 4).
        If indexed=='faces', then the array will be interpreted
        as indexed and should have shape (Nf, 3, 4)
        """
        if indexed is None:
            self._vertexColors = colors
            self._vertexColorsIndexedByFaces = None
        elif indexed == 'faces':
            self._vertexColors = None
            self._vertexColorsIndexedByFaces = colors
        else:
            raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def faceColors(self, indexed=None):
        """
        Return an array (Nf, 4) of face colors.
        If indexed=='faces', then instead return an indexed array
        (Nf, 3, 4)  (note this is just the same array with each color
        repeated three times). 
        """
        if indexed is None:
            return self._faceColors
        if indexed == 'faces':
            if self._faceColorsIndexedByFaces is None:
                if self._faceColors is not None:
                    Nf = self._faceColors.shape[0]
                    self._faceColorsIndexedByFaces = np.empty((Nf, 3, 4), dtype=(self._faceColors.dtype))
                    self._faceColorsIndexedByFaces[:] = self._faceColors.reshape(Nf, 1, 4)
            return self._faceColorsIndexedByFaces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def setFaceColors(self, colors, indexed=None):
        """
        Set the face color array (Nf, 4).
        If indexed=='faces', then the array will be interpreted
        as indexed and should have shape (Nf, 3, 4)
        """
        if indexed is None:
            self._faceColors = colors
            self._faceColorsIndexedByFaces = None
        elif indexed == 'faces':
            self._faceColors = None
            self._faceColorsIndexedByFaces = colors
        else:
            raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def faceCount(self):
        """
        Return the number of faces in the mesh.
        """
        if self._faces is not None:
            return self._faces.shape[0]
        if self._vertexesIndexedByFaces is not None:
            return self._vertexesIndexedByFaces.shape[0]

    def edgeColors(self):
        return self._edgeColors

    def _computeUnindexedVertexes(self):
        faces = self._vertexesIndexedByFaces
        verts = {}
        self._faces = np.empty((faces.shape[:2]), dtype=(np.uint))
        self._vertexes = []
        self._vertexFaces = []
        self._faceNormals = None
        self._vertexNormals = None
        for i in xrange(faces.shape[0]):
            face = faces[i]
            inds = []
            for j in range(face.shape[0]):
                pt = face[j]
                pt2 = tuple([round(x * 100000000000000.0) for x in pt])
                index = verts.get(pt2, None)
                if index is None:
                    self._vertexes.append(pt)
                    self._vertexFaces.append([])
                    index = len(self._vertexes) - 1
                    verts[pt2] = index
                self._vertexFaces[index].append(i)
                self._faces[(i, j)] = index

        self._vertexes = np.array((self._vertexes), dtype=float)

    def vertexFaces(self):
        """
        Return list mapping each vertex index to a list of face indexes that use the vertex.
        """
        if self._vertexFaces is None:
            self._vertexFaces = [[] for i in xrange(len(self.vertexes()))]
            for i in xrange(self._faces.shape[0]):
                face = self._faces[i]
                for ind in face:
                    self._vertexFaces[ind].append(i)

        return self._vertexFaces

    def _computeEdges(self):
        if not self.hasFaceIndexedData:
            nf = len(self._faces)
            edges = np.empty((nf * 3), dtype=[('i', np.uint, 2)])
            edges['i'][0:nf] = self._faces[:, :2]
            edges['i'][nf:2 * nf] = self._faces[:, 1:3]
            edges['i'][-nf:, 0] = self._faces[:, 2]
            edges['i'][-nf:, 1] = self._faces[:, 0]
            mask = edges['i'][:, 0] > edges['i'][:, 1]
            edges['i'][mask] = edges['i'][mask][:, ::-1]
            self._edges = np.unique(edges)['i']
        elif self._vertexesIndexedByFaces is not None:
            verts = self._vertexesIndexedByFaces
            edges = np.empty((verts.shape[0], 3, 2), dtype=(np.uint))
            nf = verts.shape[0]
            edges[:, 0, 0] = np.arange(nf) * 3
            edges[:, 0, 1] = edges[:, 0, 0] + 1
            edges[:, 1, 0] = edges[:, 0, 1]
            edges[:, 1, 1] = edges[:, 1, 0] + 1
            edges[:, 2, 0] = edges[:, 1, 1]
            edges[:, 2, 1] = edges[:, 0, 0]
            self._edges = edges
        else:
            raise Exception('MeshData cannot generate edges--no faces in this data.')

    def save(self):
        """Serialize this mesh to a string appropriate for disk storage"""
        import pickle
        if self._faces is not None:
            names = [
             '_vertexes', '_faces']
        else:
            names = [
             '_vertexesIndexedByFaces']
        if self._vertexColors is not None:
            names.append('_vertexColors')
        elif self._vertexColorsIndexedByFaces is not None:
            names.append('_vertexColorsIndexedByFaces')
        if self._faceColors is not None:
            names.append('_faceColors')
        elif self._faceColorsIndexedByFaces is not None:
            names.append('_faceColorsIndexedByFaces')
        state = dict([(n, getattr(self, n)) for n in names])
        return pickle.dumps(state)

    def restore(self, state):
        """Restore the state of a mesh previously saved using save()"""
        import pickle
        state = pickle.loads(state)
        for k in state:
            if isinstance(state[k], list):
                if isinstance(state[k][0], QtGui.QVector3D):
                    state[k] = [[v.x(), v.y(), v.z()] for v in state[k]]
                state[k] = np.array(state[k])
            setattr(self, k, state[k])

    @staticmethod
    def sphere(rows, cols, radius=1.0, offset=True):
        """
        Return a MeshData instance with vertexes and faces computed
        for a spherical surface.
        """
        verts = np.empty((rows + 1, cols, 3), dtype=float)
        phi = (np.arange(rows + 1) * np.pi / rows).reshape(rows + 1, 1)
        s = radius * np.sin(phi)
        verts[(Ellipsis, 2)] = radius * np.cos(phi)
        th = (np.arange(cols) * 2 * np.pi / cols).reshape(1, cols)
        if offset:
            th = th + np.pi / cols * np.arange(rows + 1).reshape(rows + 1, 1)
        verts[(Ellipsis, 0)] = s * np.cos(th)
        verts[(Ellipsis, 1)] = s * np.sin(th)
        verts = verts.reshape((rows + 1) * cols, 3)[cols - 1:-(cols - 1)]
        faces = np.empty((rows * cols * 2, 3), dtype=(np.uint))
        rowtemplate1 = (np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 0]])) % cols + np.array([[0, 0, cols]])
        rowtemplate2 = (np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 1]])) % cols + np.array([[cols, 0, cols]])
        for row in range(rows):
            start = row * cols * 2
            faces[start:start + cols] = rowtemplate1 + row * cols
            faces[start + cols:start + cols * 2] = rowtemplate2 + row * cols

        faces = faces[cols:-cols]
        vmin = cols - 1
        faces[faces < vmin] = vmin
        faces -= vmin
        vmax = verts.shape[0] - 1
        faces[faces > vmax] = vmax
        return MeshData(vertexes=verts, faces=faces)

    @staticmethod
    def cylinder(rows, cols, radius=[1.0, 1.0], length=1.0, offset=False):
        """
        Return a MeshData instance with vertexes and faces computed
        for a cylindrical surface.
        The cylinder may be tapered with different radii at each end (truncated cone)
        """
        verts = np.empty((rows + 1, cols, 3), dtype=float)
        if isinstance(radius, int):
            radius = [
             radius, radius]
        th = np.linspace(2 * np.pi, 0, cols).reshape(1, cols)
        r = np.linspace((radius[0]), (radius[1]), num=(rows + 1), endpoint=True).reshape(rows + 1, 1)
        verts[(Ellipsis, 2)] = np.linspace(0, length, num=(rows + 1), endpoint=True).reshape(rows + 1, 1)
        if offset:
            th = th + np.pi / cols * np.arange(rows + 1).reshape(rows + 1, 1)
        verts[(Ellipsis, 0)] = r * np.cos(th)
        verts[(Ellipsis, 1)] = r * np.sin(th)
        verts = verts.reshape((rows + 1) * cols, 3)
        faces = np.empty((rows * cols * 2, 3), dtype=(np.uint))
        rowtemplate1 = (np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 0]])) % cols + np.array([[0, 0, cols]])
        rowtemplate2 = (np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 1]])) % cols + np.array([[cols, 0, cols]])
        for row in range(rows):
            start = row * cols * 2
            faces[start:start + cols] = rowtemplate1 + row * cols
            faces[start + cols:start + cols * 2] = rowtemplate2 + row * cols

        return MeshData(vertexes=verts, faces=faces)