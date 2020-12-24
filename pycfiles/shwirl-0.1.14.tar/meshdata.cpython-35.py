# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/geometry/meshdata.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 22793 bytes
import numpy as np
from ..ext.six.moves import xrange

def _fix_colors(colors):
    colors = np.asarray(colors)
    if colors.ndim not in (2, 3):
        raise ValueError('colors must have 2 or 3 dimensions')
    if colors.shape[(-1)] not in (3, 4):
        raise ValueError('colors must have 3 or 4 elements')
    if colors.shape[(-1)] == 3:
        pad = np.ones((len(colors), 1), colors.dtype)
        if colors.ndim == 3:
            pad = pad[:, :, np.newaxis]
        colors = np.concatenate((colors, pad), axis=-1)
    return colors


class MeshData(object):
    __doc__ = "\n    Class for storing and operating on 3D mesh data.\n\n    Parameters\n    ----------\n    vertices : ndarray, shape (Nv, 3)\n        Vertex coordinates. If faces is not specified, then this will\n        instead be interpreted as (Nf, 3, 3) array of coordinates.\n    faces : ndarray, shape (Nf, 3)\n        Indices into the vertex array.\n    edges : None\n        [not available yet]\n    vertex_colors : ndarray, shape (Nv, 4)\n        Vertex colors. If faces is not specified, this will be\n        interpreted as (Nf, 3, 4) array of colors.\n    face_colors : ndarray, shape (Nf, 4)\n        Face colors.\n\n    Notes\n    -----\n    All arguments are optional.\n\n    The object may contain:\n\n    - list of vertex locations\n    - list of edges\n    - list of triangles\n    - colors per vertex, edge, or tri\n    - normals per vertex or tri\n\n    This class handles conversion between the standard\n    [list of vertices, list of faces] format (suitable for use with\n    glDrawElements) and 'indexed' [list of vertices] format (suitable\n    for use with glDrawArrays). It will automatically compute face normal\n    vectors as well as averaged vertex normal vectors.\n\n    The class attempts to be as efficient as possible in caching conversion\n    results and avoiding unnecessary conversions.\n    "

    def __init__(self, vertices=None, faces=None, edges=None, vertex_colors=None, face_colors=None):
        self._vertices = None
        self._vertices_indexed_by_faces = None
        self._vertices_indexed_by_edges = None
        self._faces = None
        self._edges = None
        self._edges_indexed_by_faces = None
        self._vertex_faces = None
        self._vertex_edges = None
        self._vertex_normals = None
        self._vertex_normals_indexed_by_faces = None
        self._vertex_colors = None
        self._vertex_colors_indexed_by_faces = None
        self._vertex_colors_indexed_by_edges = None
        self._face_normals = None
        self._face_normals_indexed_by_faces = None
        self._face_colors = None
        self._face_colors_indexed_by_faces = None
        self._face_colors_indexed_by_edges = None
        self._edge_colors = None
        self._edge_colors_indexed_by_edges = None
        if vertices is not None:
            if faces is None:
                self.set_vertices(vertices, indexed='faces')
                if vertex_colors is not None:
                    self.set_vertex_colors(vertex_colors, indexed='faces')
                if face_colors is not None:
                    self.set_face_colors(face_colors, indexed='faces')
        else:
            self.set_vertices(vertices)
            self.set_faces(faces)
        if vertex_colors is not None:
            self.set_vertex_colors(vertex_colors)
        if face_colors is not None:
            self.set_face_colors(face_colors)

    def get_faces(self):
        """Array (Nf, 3) of vertex indices, three per triangular face.

        If faces have not been computed for this mesh, returns None.
        """
        return self._faces

    def get_edges(self, indexed=None):
        """Edges of the mesh
        
        Parameters
        ----------
        indexed : str | None
           If indexed is None, return (Nf, 3) array of vertex indices,
           two per edge in the mesh.
           If indexed is 'faces', then return (Nf, 3, 2) array of vertex
           indices with 3 edges per face, and two vertices per edge.

        Returns
        -------
        edges : ndarray
            The edges.
        """
        if indexed is None:
            if self._edges is None:
                self._compute_edges(indexed=None)
            return self._edges
        if indexed == 'faces':
            if self._edges_indexed_by_faces is None:
                self._compute_edges(indexed='faces')
            return self._edges_indexed_by_faces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def set_faces(self, faces):
        """Set the faces

        Parameters
        ----------
        faces : ndarray
            (Nf, 3) array of faces. Each row in the array contains
            three indices into the vertex array, specifying the three corners
            of a triangular face.
        """
        self._faces = faces
        self._edges = None
        self._edges_indexed_by_faces = None
        self._vertex_faces = None
        self._vertices_indexed_by_faces = None
        self.reset_normals()
        self._vertex_colors_indexed_by_faces = None
        self._face_colors_indexed_by_faces = None

    def get_vertices(self, indexed=None):
        """Get the vertices

        Parameters
        ----------
        indexed : str | None
            If Note, return an array (N,3) of the positions of vertices in
            the mesh. By default, each unique vertex appears only once.
            If indexed is 'faces', then the array will instead contain three
            vertices per face in the mesh (and a single vertex may appear more
            than once in the array).

        Returns
        -------
        vertices : ndarray
            The vertices.
        """
        if indexed is None:
            if self._vertices is None and self._vertices_indexed_by_faces is not None:
                self._compute_unindexed_vertices()
            return self._vertices
        if indexed == 'faces':
            if self._vertices_indexed_by_faces is None and self._vertices is not None:
                self._vertices_indexed_by_faces = self._vertices[self.get_faces()]
            return self._vertices_indexed_by_faces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def get_bounds(self):
        """Get the mesh bounds

        Returns
        -------
        bounds : list
            A list of tuples of mesh bounds.
        """
        if self._vertices_indexed_by_faces is not None:
            v = self._vertices_indexed_by_faces
        else:
            if self._vertices is not None:
                v = self._vertices
            else:
                return
        bounds = [(v[:, ax].min(), v[:, ax].max()) for ax in range(v.shape[1])]
        return bounds

    def set_vertices(self, verts=None, indexed=None, reset_normals=True):
        """Set the mesh vertices

        Parameters
        ----------
        verts : ndarray | None
            The array (Nv, 3) of vertex coordinates.
        indexed : str | None
            If indexed=='faces', then the data must have shape (Nf, 3, 3) and
            is assumed to be already indexed as a list of faces. This will
            cause any pre-existing normal vectors to be cleared unless
            reset_normals=False.
        reset_normals : bool
            If True, reset the normals.
        """
        if indexed is None:
            if verts is not None:
                self._vertices = verts
            self._vertices_indexed_by_faces = None
        else:
            if indexed == 'faces':
                self._vertices = None
                if verts is not None:
                    self._vertices_indexed_by_faces = verts
            else:
                raise Exception("Invalid indexing mode. Accepts: None, 'faces'")
        if reset_normals:
            self.reset_normals()

    def reset_normals(self):
        self._vertex_normals = None
        self._vertex_normals_indexed_by_faces = None
        self._face_normals = None
        self._face_normals_indexed_by_faces = None

    def has_face_indexed_data(self):
        """Return True if this object already has vertex positions indexed
        by face"""
        return self._vertices_indexed_by_faces is not None

    def has_edge_indexed_data(self):
        return self._vertices_indexed_by_edges is not None

    def has_vertex_color(self):
        """Return True if this data set has vertex color information"""
        for v in (self._vertex_colors, self._vertex_colors_indexed_by_faces,
         self._vertex_colors_indexed_by_edges):
            if v is not None:
                return True

        return False

    def has_face_color(self):
        """Return True if this data set has face color information"""
        for v in (self._face_colors, self._face_colors_indexed_by_faces,
         self._face_colors_indexed_by_edges):
            if v is not None:
                return True

        return False

    def get_face_normals(self, indexed=None):
        """Get face normals

        Parameters
        ----------
        indexed : str | None
            If None, return an array (Nf, 3) of normal vectors for each face.
            If 'faces', then instead return an indexed array (Nf, 3, 3)
            (this is just the same array with each vector copied three times).

        Returns
        -------
        normals : ndarray
            The normals.
        """
        if self._face_normals is None:
            v = self.get_vertices(indexed='faces')
            self._face_normals = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
        if indexed is None:
            return self._face_normals
        if indexed == 'faces':
            if self._face_normals_indexed_by_faces is None:
                norms = np.empty((self._face_normals.shape[0], 3, 3), dtype=np.float32)
                norms[:] = self._face_normals[:, np.newaxis, :]
                self._face_normals_indexed_by_faces = norms
            return self._face_normals_indexed_by_faces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def get_vertex_normals(self, indexed=None):
        """Get vertex normals

        Parameters
        ----------
        indexed : str | None
            If None, return an (N, 3) array of normal vectors with one entry
            per unique vertex in the mesh. If indexed is 'faces', then the
            array will contain three normal vectors per face (and some
            vertices may be repeated).

        Returns
        -------
        normals : ndarray
            The normals.
        """
        if self._vertex_normals is None:
            faceNorms = self.get_face_normals()
            vertFaces = self.get_vertex_faces()
            self._vertex_normals = np.empty(self._vertices.shape, dtype=np.float32)
            for vindex in xrange(self._vertices.shape[0]):
                faces = vertFaces[vindex]
                if len(faces) == 0:
                    self._vertex_normals[vindex] = (0, 0, 0)
                    continue
                    norms = faceNorms[faces]
                    norm = norms.sum(axis=0)
                    renorm = (norm ** 2).sum() ** 0.5
                    if renorm > 0:
                        norm /= renorm
                    self._vertex_normals[vindex] = norm

        if indexed is None:
            return self._vertex_normals
        if indexed == 'faces':
            return self._vertex_normals[self.get_faces()]
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def get_vertex_colors(self, indexed=None):
        """Get vertex colors

        Parameters
        ----------
        indexed : str | None
            If None, return an array (Nv, 4) of vertex colors.
            If indexed=='faces', then instead return an indexed array
            (Nf, 3, 4).

        Returns
        -------
        colors : ndarray
            The vertex colors.
        """
        if indexed is None:
            return self._vertex_colors
        if indexed == 'faces':
            if self._vertex_colors_indexed_by_faces is None:
                self._vertex_colors_indexed_by_faces = self._vertex_colors[self.get_faces()]
            return self._vertex_colors_indexed_by_faces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def set_vertex_colors(self, colors, indexed=None):
        """Set the vertex color array

        Parameters
        ----------
        colors : array
            Array of colors. Must have shape (Nv, 4) (indexing by vertex)
            or shape (Nf, 3, 4) (vertices indexed by face).
        indexed : str | None
            Should be 'faces' if colors are indexed by faces.
        """
        colors = _fix_colors(np.asarray(colors))
        if indexed is None:
            if colors.ndim != 2:
                raise ValueError('colors must be 2D if indexed is None')
            if colors.shape[0] != self.n_vertices:
                raise ValueError('incorrect number of colors %s, expected %s' % (
                 colors.shape[0], self.n_vertices))
            self._vertex_colors = colors
            self._vertex_colors_indexed_by_faces = None
        else:
            if indexed == 'faces':
                if colors.ndim != 3:
                    raise ValueError('colors must be 3D if indexed is "faces"')
                if colors.shape[0] != self.n_faces:
                    raise ValueError('incorrect number of faces')
                self._vertex_colors = None
                self._vertex_colors_indexed_by_faces = colors
            else:
                raise ValueError('indexed must be None or "faces"')

    def get_face_colors(self, indexed=None):
        """Get the face colors

        Parameters
        ----------
        indexed : str | None
            If indexed is None, return (Nf, 4) array of face colors.
            If indexed=='faces', then instead return an indexed array
            (Nf, 3, 4)  (note this is just the same array with each color
            repeated three times).
        
        Returns
        -------
        colors : ndarray
            The colors.
        """
        if indexed is None:
            return self._face_colors
        if indexed == 'faces':
            if self._face_colors_indexed_by_faces is None and self._face_colors is not None:
                Nf = self._face_colors.shape[0]
                self._face_colors_indexed_by_faces = np.empty((Nf, 3, 4), dtype=self._face_colors.dtype)
                self._face_colors_indexed_by_faces[:] = self._face_colors.reshape(Nf, 1, 4)
            return self._face_colors_indexed_by_faces
        raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def set_face_colors(self, colors, indexed=None):
        """Set the face color array

        Parameters
        ----------
        colors : array
            Array of colors. Must have shape (Nf, 4) (indexed by face),
            or shape (Nf, 3, 4) (face colors indexed by faces).
        indexed : str | None
            Should be 'faces' if colors are indexed by faces.
        """
        colors = _fix_colors(colors)
        if colors.shape[0] != self.n_faces:
            raise ValueError('incorrect number of colors %s, expected %s' % (
             colors.shape[0], self.n_faces))
        if indexed is None:
            if colors.ndim != 2:
                raise ValueError('colors must be 2D if indexed is None')
            self._face_colors = colors
            self._face_colors_indexed_by_faces = None
        else:
            if indexed == 'faces':
                if colors.ndim != 3:
                    raise ValueError('colors must be 3D if indexed is "faces"')
                self._face_colors = None
                self._face_colors_indexed_by_faces = colors
            else:
                raise ValueError('indexed must be None or "faces"')

    @property
    def n_faces(self):
        """The number of faces in the mesh"""
        if self._faces is not None:
            return self._faces.shape[0]
        if self._vertices_indexed_by_faces is not None:
            return self._vertices_indexed_by_faces.shape[0]

    @property
    def n_vertices(self):
        """The number of vertices in the mesh"""
        if self._vertices is None:
            self._compute_unindexed_vertices()
        return len(self._vertices)

    def get_edge_colors(self):
        return self._edge_colors

    def _compute_unindexed_vertices(self):
        faces = self._vertices_indexed_by_faces
        verts = {}
        self._faces = np.empty(faces.shape[:2], dtype=np.uint32)
        self._vertices = []
        self._vertex_faces = []
        self._face_normals = None
        self._vertex_normals = None
        for i in xrange(faces.shape[0]):
            face = faces[i]
            for j in range(face.shape[0]):
                pt = face[j]
                pt2 = tuple([round(x * 100000000000000.0) for x in pt])
                index = verts.get(pt2, None)
                if index is None:
                    self._vertices.append(pt)
                    self._vertex_faces.append([])
                    index = len(self._vertices) - 1
                    verts[pt2] = index
                self._vertex_faces[index].append(i)
                self._faces[(i, j)] = index

        self._vertices = np.array(self._vertices, dtype=np.float32)

    def get_vertex_faces(self):
        """
        List mapping each vertex index to a list of face indices that use it.
        """
        if self._vertex_faces is None:
            self._vertex_faces = [[] for i in xrange(len(self.get_vertices()))]
            for i in xrange(self._faces.shape[0]):
                face = self._faces[i]
                for ind in face:
                    self._vertex_faces[ind].append(i)

        return self._vertex_faces

    def _compute_edges(self, indexed=None):
        if indexed is None:
            if self._faces is not None:
                nf = len(self._faces)
                edges = np.empty(nf * 3, dtype=[('i', np.uint32, 2)])
                edges['i'][0:nf] = self._faces[:, :2]
                edges['i'][nf:2 * nf] = self._faces[:, 1:3]
                edges['i'][-nf:, 0] = self._faces[:, 2]
                edges['i'][-nf:, 1] = self._faces[:, 0]
                mask = edges['i'][:, 0] > edges['i'][:, 1]
                edges['i'][mask] = edges['i'][mask][:, ::-1]
                self._edges = np.unique(edges)['i']
            else:
                raise Exception('MeshData cannot generate edges--no faces in this data.')
        else:
            if indexed == 'faces':
                if self._vertices_indexed_by_faces is not None:
                    verts = self._vertices_indexed_by_faces
                    edges = np.empty((verts.shape[0], 3, 2), dtype=np.uint32)
                    nf = verts.shape[0]
                    edges[:, 0, 0] = np.arange(nf) * 3
                    edges[:, 0, 1] = edges[:, 0, 0] + 1
                    edges[:, 1, 0] = edges[:, 0, 1]
                    edges[:, 1, 1] = edges[:, 1, 0] + 1
                    edges[:, 2, 0] = edges[:, 1, 1]
                    edges[:, 2, 1] = edges[:, 0, 0]
                    self._edges_indexed_by_faces = edges
                else:
                    raise Exception('MeshData cannot generate edges--no faces in this data.')
            else:
                raise Exception("Invalid indexing mode. Accepts: None, 'faces'")

    def save(self):
        """Serialize this mesh to a string appropriate for disk storage

        Returns
        -------
        state : dict
            The state.
        """
        import pickle
        if self._faces is not None:
            names = [
             '_vertices', '_faces']
        else:
            names = [
             '_vertices_indexed_by_faces']
        if self._vertex_colors is not None:
            names.append('_vertex_colors')
        else:
            if self._vertex_colors_indexed_by_faces is not None:
                names.append('_vertex_colors_indexed_by_faces')
            if self._face_colors is not None:
                names.append('_face_colors')
            elif self._face_colors_indexed_by_faces is not None:
                names.append('_face_colors_indexed_by_faces')
        state = dict([(n, getattr(self, n)) for n in names])
        return pickle.dumps(state)

    def restore(self, state):
        """Restore the state of a mesh previously saved using save()

        Parameters
        ----------
        state : dict
            The previous state.
        """
        import pickle
        state = pickle.loads(state)
        for k in state:
            if isinstance(state[k], list):
                state[k] = np.array(state[k])
            setattr(self, k, state[k])