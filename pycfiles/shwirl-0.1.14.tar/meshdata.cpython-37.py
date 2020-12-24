# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/geometry/meshdata.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 22793 bytes
import numpy as np
from ext.six.moves import xrange

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
        colors = np.concatenate((colors, pad), axis=(-1))
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
            if self._vertices is None:
                if self._vertices_indexed_by_faces is not None:
                    self._compute_unindexed_vertices()
            return self._vertices
        if indexed == 'faces':
            if self._vertices_indexed_by_faces is None:
                if self._vertices is not None:
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
                norms = np.empty((self._face_normals.shape[0], 3, 3), dtype=(np.float32))
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
            self._vertex_normals = np.empty((self._vertices.shape), dtype=(np.float32))
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
            if self._face_colors_indexed_by_faces is None:
                if self._face_colors is not None:
                    Nf = self._face_colors.shape[0]
                    self._face_colors_indexed_by_faces = np.empty((Nf, 3, 4), dtype=(self._face_colors.dtype))
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
        elif indexed is None:
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
        self._faces = np.empty((faces.shape[:2]), dtype=(np.uint32))
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

        self._vertices = np.array((self._vertices), dtype=(np.float32))

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

    def _compute_edges--- This code section failed: ---

 L. 523         0  LOAD_FAST                'indexed'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
              6_8  POP_JUMP_IF_FALSE   312  'to 312'

 L. 524        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _faces
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
            18_20  POP_JUMP_IF_FALSE   300  'to 300'

 L. 526        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _faces
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'nf'

 L. 527        32  LOAD_GLOBAL              np
               34  LOAD_ATTR                empty
               36  LOAD_FAST                'nf'
               38  LOAD_CONST               3
               40  BINARY_MULTIPLY  
               42  LOAD_STR                 'i'
               44  LOAD_GLOBAL              np
               46  LOAD_ATTR                uint32
               48  LOAD_CONST               2
               50  BUILD_TUPLE_3         3 
               52  BUILD_LIST_1          1 
               54  LOAD_CONST               ('dtype',)
               56  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               58  STORE_FAST               'edges'

 L. 528        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _faces
               64  LOAD_CONST               None
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  LOAD_CONST               None
               72  LOAD_CONST               2
               74  BUILD_SLICE_2         2 
               76  BUILD_TUPLE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'edges'
               82  LOAD_STR                 'i'
               84  BINARY_SUBSCR    
               86  LOAD_CONST               0
               88  LOAD_FAST                'nf'
               90  BUILD_SLICE_2         2 
               92  STORE_SUBSCR     

 L. 529        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _faces
               98  LOAD_CONST               None
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  LOAD_CONST               1
              106  LOAD_CONST               3
              108  BUILD_SLICE_2         2 
              110  BUILD_TUPLE_2         2 
              112  BINARY_SUBSCR    
              114  LOAD_FAST                'edges'
              116  LOAD_STR                 'i'
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'nf'
              122  LOAD_CONST               2
              124  LOAD_FAST                'nf'
              126  BINARY_MULTIPLY  
              128  BUILD_SLICE_2         2 
              130  STORE_SUBSCR     

 L. 530       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _faces
              136  LOAD_CONST               None
              138  LOAD_CONST               None
              140  BUILD_SLICE_2         2 
              142  LOAD_CONST               2
              144  BUILD_TUPLE_2         2 
              146  BINARY_SUBSCR    
              148  LOAD_FAST                'edges'
              150  LOAD_STR                 'i'
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'nf'
              156  UNARY_NEGATIVE   
              158  LOAD_CONST               None
              160  BUILD_SLICE_2         2 
              162  LOAD_CONST               0
              164  BUILD_TUPLE_2         2 
              166  STORE_SUBSCR     

 L. 531       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _faces
              172  LOAD_CONST               None
              174  LOAD_CONST               None
              176  BUILD_SLICE_2         2 
              178  LOAD_CONST               0
              180  BUILD_TUPLE_2         2 
              182  BINARY_SUBSCR    
              184  LOAD_FAST                'edges'
              186  LOAD_STR                 'i'
              188  BINARY_SUBSCR    
              190  LOAD_FAST                'nf'
              192  UNARY_NEGATIVE   
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  LOAD_CONST               1
              200  BUILD_TUPLE_2         2 
              202  STORE_SUBSCR     

 L. 533       204  LOAD_FAST                'edges'
              206  LOAD_STR                 'i'
              208  BINARY_SUBSCR    
              210  LOAD_CONST               None
              212  LOAD_CONST               None
              214  BUILD_SLICE_2         2 
              216  LOAD_CONST               0
              218  BUILD_TUPLE_2         2 
              220  BINARY_SUBSCR    
              222  LOAD_FAST                'edges'
              224  LOAD_STR                 'i'
              226  BINARY_SUBSCR    
              228  LOAD_CONST               None
              230  LOAD_CONST               None
              232  BUILD_SLICE_2         2 
              234  LOAD_CONST               1
              236  BUILD_TUPLE_2         2 
              238  BINARY_SUBSCR    
              240  COMPARE_OP               >
              242  STORE_FAST               'mask'

 L. 534       244  LOAD_FAST                'edges'
              246  LOAD_STR                 'i'
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'mask'
              252  BINARY_SUBSCR    
              254  LOAD_CONST               None
              256  LOAD_CONST               None
              258  BUILD_SLICE_2         2 
              260  LOAD_CONST               None
              262  LOAD_CONST               None
              264  LOAD_CONST               -1
              266  BUILD_SLICE_3         3 
              268  BUILD_TUPLE_2         2 
              270  BINARY_SUBSCR    
              272  LOAD_FAST                'edges'
              274  LOAD_STR                 'i'
              276  BINARY_SUBSCR    
              278  LOAD_FAST                'mask'
              280  STORE_SUBSCR     

 L. 536       282  LOAD_GLOBAL              np
              284  LOAD_METHOD              unique
              286  LOAD_FAST                'edges'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  LOAD_STR                 'i'
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'self'
              296  STORE_ATTR               _edges
              298  JUMP_FORWARD        600  'to 600'
            300_0  COME_FROM            18  '18'

 L. 538       300  LOAD_GLOBAL              Exception
              302  LOAD_STR                 'MeshData cannot generate edges--no faces in this data.'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  RAISE_VARARGS_1       1  'exception instance'
          308_310  JUMP_FORWARD        600  'to 600'
            312_0  COME_FROM             6  '6'

 L. 540       312  LOAD_FAST                'indexed'
              314  LOAD_STR                 'faces'
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   592  'to 592'

 L. 541       322  LOAD_FAST                'self'
              324  LOAD_ATTR                _vertices_indexed_by_faces
              326  LOAD_CONST               None
              328  COMPARE_OP               is-not
          330_332  POP_JUMP_IF_FALSE   582  'to 582'

 L. 542       334  LOAD_FAST                'self'
              336  LOAD_ATTR                _vertices_indexed_by_faces
              338  STORE_FAST               'verts'

 L. 543       340  LOAD_GLOBAL              np
              342  LOAD_ATTR                empty
              344  LOAD_FAST                'verts'
              346  LOAD_ATTR                shape
              348  LOAD_CONST               0
              350  BINARY_SUBSCR    
              352  LOAD_CONST               3
              354  LOAD_CONST               2
              356  BUILD_TUPLE_3         3 
              358  LOAD_GLOBAL              np
              360  LOAD_ATTR                uint32
              362  LOAD_CONST               ('dtype',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  STORE_FAST               'edges'

 L. 544       368  LOAD_FAST                'verts'
              370  LOAD_ATTR                shape
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  STORE_FAST               'nf'

 L. 545       378  LOAD_GLOBAL              np
              380  LOAD_METHOD              arange
              382  LOAD_FAST                'nf'
              384  CALL_METHOD_1         1  '1 positional argument'
              386  LOAD_CONST               3
              388  BINARY_MULTIPLY  
              390  LOAD_FAST                'edges'
              392  LOAD_CONST               None
              394  LOAD_CONST               None
              396  BUILD_SLICE_2         2 
              398  LOAD_CONST               0
              400  LOAD_CONST               0
              402  BUILD_TUPLE_3         3 
              404  STORE_SUBSCR     

 L. 546       406  LOAD_FAST                'edges'
              408  LOAD_CONST               None
              410  LOAD_CONST               None
              412  BUILD_SLICE_2         2 
              414  LOAD_CONST               0
              416  LOAD_CONST               0
              418  BUILD_TUPLE_3         3 
              420  BINARY_SUBSCR    
              422  LOAD_CONST               1
              424  BINARY_ADD       
              426  LOAD_FAST                'edges'
              428  LOAD_CONST               None
              430  LOAD_CONST               None
              432  BUILD_SLICE_2         2 
              434  LOAD_CONST               0
              436  LOAD_CONST               1
              438  BUILD_TUPLE_3         3 
              440  STORE_SUBSCR     

 L. 547       442  LOAD_FAST                'edges'
              444  LOAD_CONST               None
              446  LOAD_CONST               None
              448  BUILD_SLICE_2         2 
              450  LOAD_CONST               0
              452  LOAD_CONST               1
              454  BUILD_TUPLE_3         3 
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'edges'
              460  LOAD_CONST               None
              462  LOAD_CONST               None
              464  BUILD_SLICE_2         2 
              466  LOAD_CONST               1
              468  LOAD_CONST               0
              470  BUILD_TUPLE_3         3 
              472  STORE_SUBSCR     

 L. 548       474  LOAD_FAST                'edges'
              476  LOAD_CONST               None
              478  LOAD_CONST               None
              480  BUILD_SLICE_2         2 
              482  LOAD_CONST               1
              484  LOAD_CONST               0
              486  BUILD_TUPLE_3         3 
              488  BINARY_SUBSCR    
              490  LOAD_CONST               1
              492  BINARY_ADD       
              494  LOAD_FAST                'edges'
              496  LOAD_CONST               None
              498  LOAD_CONST               None
              500  BUILD_SLICE_2         2 
              502  LOAD_CONST               1
              504  LOAD_CONST               1
              506  BUILD_TUPLE_3         3 
              508  STORE_SUBSCR     

 L. 549       510  LOAD_FAST                'edges'
              512  LOAD_CONST               None
              514  LOAD_CONST               None
              516  BUILD_SLICE_2         2 
              518  LOAD_CONST               1
              520  LOAD_CONST               1
              522  BUILD_TUPLE_3         3 
              524  BINARY_SUBSCR    
              526  LOAD_FAST                'edges'
              528  LOAD_CONST               None
              530  LOAD_CONST               None
              532  BUILD_SLICE_2         2 
              534  LOAD_CONST               2
              536  LOAD_CONST               0
              538  BUILD_TUPLE_3         3 
              540  STORE_SUBSCR     

 L. 550       542  LOAD_FAST                'edges'
              544  LOAD_CONST               None
              546  LOAD_CONST               None
              548  BUILD_SLICE_2         2 
              550  LOAD_CONST               0
              552  LOAD_CONST               0
              554  BUILD_TUPLE_3         3 
              556  BINARY_SUBSCR    
              558  LOAD_FAST                'edges'
              560  LOAD_CONST               None
              562  LOAD_CONST               None
              564  BUILD_SLICE_2         2 
              566  LOAD_CONST               2
              568  LOAD_CONST               1
              570  BUILD_TUPLE_3         3 
              572  STORE_SUBSCR     

 L. 551       574  LOAD_FAST                'edges'
              576  LOAD_FAST                'self'
              578  STORE_ATTR               _edges_indexed_by_faces
              580  JUMP_FORWARD        590  'to 590'
            582_0  COME_FROM           330  '330'

 L. 553       582  LOAD_GLOBAL              Exception
              584  LOAD_STR                 'MeshData cannot generate edges--no faces in this data.'
              586  CALL_FUNCTION_1       1  '1 positional argument'
            588_0  COME_FROM           298  '298'
              588  RAISE_VARARGS_1       1  'exception instance'
            590_0  COME_FROM           580  '580'
              590  JUMP_FORWARD        600  'to 600'
            592_0  COME_FROM           318  '318'

 L. 556       592  LOAD_GLOBAL              Exception
              594  LOAD_STR                 "Invalid indexing mode. Accepts: None, 'faces'"
              596  CALL_FUNCTION_1       1  '1 positional argument'
              598  RAISE_VARARGS_1       1  'exception instance'
            600_0  COME_FROM           590  '590'
            600_1  COME_FROM           308  '308'

Parse error at or near `COME_FROM' instruction at offset 588_0

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
            elif self._face_colors is not None:
                names.append('_face_colors')
            else:
                if self._face_colors_indexed_by_faces is not None:
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