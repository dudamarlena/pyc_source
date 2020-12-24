# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/transforms/linear.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 15677 bytes
from __future__ import division
import numpy as np
from ...util import transforms
from ...geometry import Rect
from ._util import arg_to_vec4, as_vec4
from .base_transform import BaseTransform

class NullTransform(BaseTransform):
    __doc__ = ' Transform having no effect on coordinates (identity transform).\n    '
    glsl_map = 'vec4 null_transform_map(vec4 pos) {return pos;}'
    glsl_imap = 'vec4 null_transform_imap(vec4 pos) {return pos;}'
    Linear = True
    Orthogonal = True
    NonScaling = True
    Isometric = True

    @arg_to_vec4
    def map(self, coords):
        """Map coordinates

        Parameters
        ----------
        coords : array-like
            Coordinates to map.
        """
        return coords

    def imap(self, coords):
        """Inverse map coordinates

        Parameters
        ----------
        coords : array-like
            Coordinates to inverse map.
        """
        return coords

    def __mul__(self, tr):
        return tr

    def __rmul__(self, tr):
        return tr


class STTransform(BaseTransform):
    __doc__ = ' Transform performing only scale and translate, in that order.\n\n    Parameters\n    ----------\n    scale : array-like\n        Scale factors for X, Y, Z axes.\n    translate : array-like\n        Scale factors for X, Y, Z axes.\n    '
    glsl_map = '\n        vec4 st_transform_map(vec4 pos) {\n            return vec4(pos.xyz * $scale.xyz + $translate.xyz * pos.w, pos.w);\n        }\n    '
    glsl_imap = '\n        vec4 st_transform_imap(vec4 pos) {\n            return vec4((pos.xyz - $translate.xyz * pos.w) / $scale.xyz,\n                        pos.w);\n        }\n    '
    Linear = True
    Orthogonal = True
    NonScaling = False
    Isometric = False

    def __init__(self, scale=None, translate=None):
        super(STTransform, self).__init__()
        self._scale = np.ones(4, dtype=(np.float32))
        self._translate = np.zeros(4, dtype=(np.float32))
        s = (1.0, 1.0, 1.0, 1.0) if scale is None else as_vec4(scale, default=(1, 1,
                                                                               1,
                                                                               1))
        t = (0.0, 0.0, 0.0, 0.0) if translate is None else as_vec4(translate, default=(0,
                                                                                       0,
                                                                                       0,
                                                                                       0))
        self._set_st(s, t)
        self._update_shaders()

    @arg_to_vec4
    def map(self, coords):
        """Map coordinates

        Parameters
        ----------
        coords : array-like
            Coordinates to map.

        Returns
        -------
        coords : ndarray
            Coordinates.
        """
        m = np.empty(coords.shape)
        m[:, :3] = coords[:, :3] * self.scale[np.newaxis, :3] + coords[:, 3:] * self.translate[np.newaxis, :3]
        m[:, 3] = coords[:, 3]
        return m

    @arg_to_vec4
    def imap(self, coords):
        """Invert map coordinates

        Parameters
        ----------
        coords : array-like
            Coordinates to inverse map.

        Returns
        -------
        coords : ndarray
            Coordinates.
        """
        m = np.empty(coords.shape)
        m[:, :3] = (coords[:, :3] - coords[:, 3:] * self.translate[np.newaxis, :3]) / self.scale[np.newaxis, :3]
        m[:, 3] = coords[:, 3]
        return m

    def shader_map(self):
        return self._shader_map

    def shader_imap(self):
        return self._shader_imap

    @property
    def scale(self):
        return self._scale.copy()

    @scale.setter
    def scale(self, s):
        s = as_vec4(s, default=(1, 1, 1, 1))
        self._set_st(scale=s)

    @property
    def translate(self):
        return self._translate.copy()

    @translate.setter
    def translate(self, t):
        t = as_vec4(t, default=(0, 0, 0, 0))
        self._set_st(translate=t)

    def _set_st(self, scale=None, translate=None, update=True):
        need_update = False
        if scale is not None:
            if not np.all(scale == self._scale):
                self._scale[:] = scale
                need_update = True
        if translate is not None:
            if not np.all(translate == self._translate):
                self._translate[:] = translate
                need_update = True
        if update:
            if need_update:
                self._update_shaders()
                self.update()

    def _update_shaders(self):
        self._shader_map['scale'] = self.scale
        self._shader_map['translate'] = self.translate
        self._shader_imap['scale'] = self.scale
        self._shader_imap['translate'] = self.translate

    def move(self, move):
        """Change the translation of this transform by the amount given.

        Parameters
        ----------
        move : array-like
            The values to be added to the current translation of the transform.
        """
        move = as_vec4(move, default=(0, 0, 0, 0))
        self.translate = self.translate + move

    def zoom(self, zoom, center=(0, 0, 0), mapped=True):
        """Update the transform such that its scale factor is changed, but
        the specified center point is left unchanged.

        Parameters
        ----------
        zoom : array-like
            Values to multiply the transform's current scale
            factors.
        center : array-like
            The center point around which the scaling will take place.
        mapped : bool
            Whether *center* is expressed in mapped coordinates (True) or
            unmapped coordinates (False).
        """
        zoom = as_vec4(zoom, default=(1, 1, 1, 1))
        center = as_vec4(center, default=(0, 0, 0, 0))
        scale = self.scale * zoom
        if mapped:
            trans = center - (center - self.translate) * zoom
        else:
            trans = self.scale * (1 - zoom) * center + self.translate
        self._set_st(scale=scale, translate=trans)

    def as_matrix(self):
        m = MatrixTransform()
        m.scale(self.scale)
        m.translate(self.translate)
        return m

    @classmethod
    def from_mapping(cls, x0, x1):
        """ Create an STTransform from the given mapping

        See `set_mapping` for details.

        Parameters
        ----------
        x0 : array-like
            Start.
        x1 : array-like
            End.

        Returns
        -------
        t : instance of STTransform
            The transform.
        """
        t = cls()
        t.set_mapping(x0, x1)
        return t

    def set_mapping--- This code section failed: ---

 L. 274         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'x0'
                4  LOAD_GLOBAL              Rect
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 275        10  LOAD_FAST                'x0'
               12  LOAD_METHOD              _transform_in
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  LOAD_CONST               None
               18  LOAD_CONST               3
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'x0'
             26_0  COME_FROM             8  '8'

 L. 276        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'x1'
               30  LOAD_GLOBAL              Rect
               32  CALL_FUNCTION_2       2  '2 positional arguments'
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L. 277        36  LOAD_FAST                'x1'
               38  LOAD_METHOD              _transform_in
               40  CALL_METHOD_0         0  '0 positional arguments'
               42  LOAD_CONST               None
               44  LOAD_CONST               3
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  STORE_FAST               'x1'
             52_0  COME_FROM            34  '34'

 L. 279        52  LOAD_GLOBAL              np
               54  LOAD_METHOD              asarray
               56  LOAD_FAST                'x0'
               58  CALL_METHOD_1         1  '1 positional argument'
               60  STORE_FAST               'x0'

 L. 280        62  LOAD_GLOBAL              np
               64  LOAD_METHOD              asarray
               66  LOAD_FAST                'x1'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  STORE_FAST               'x1'

 L. 281        72  LOAD_FAST                'x0'
               74  LOAD_ATTR                ndim
               76  LOAD_CONST               2
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_TRUE    120  'to 120'
               82  LOAD_FAST                'x0'
               84  LOAD_ATTR                shape
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  LOAD_CONST               2
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_TRUE    120  'to 120'
               96  LOAD_FAST                'x1'
               98  LOAD_ATTR                ndim
              100  LOAD_CONST               2
              102  COMPARE_OP               !=
              104  POP_JUMP_IF_TRUE    120  'to 120'

 L. 282       106  LOAD_FAST                'x1'
              108  LOAD_ATTR                shape
              110  LOAD_CONST               0
              112  BINARY_SUBSCR    
              114  LOAD_CONST               2
              116  COMPARE_OP               !=
              118  POP_JUMP_IF_FALSE   128  'to 128'
            120_0  COME_FROM           104  '104'
            120_1  COME_FROM            94  '94'
            120_2  COME_FROM            80  '80'

 L. 283       120  LOAD_GLOBAL              TypeError
              122  LOAD_STR                 'set_mapping requires array inputs of shape (2, N).'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L. 285       128  LOAD_FAST                'x0'
              130  LOAD_CONST               1
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'x0'
              136  LOAD_CONST               0
              138  BINARY_SUBSCR    
              140  BINARY_SUBTRACT  
              142  STORE_FAST               'denom'

 L. 286       144  LOAD_FAST                'denom'
              146  LOAD_CONST               0
              148  COMPARE_OP               ==
              150  STORE_FAST               'mask'

 L. 287       152  LOAD_CONST               1.0
              154  LOAD_FAST                'denom'
              156  LOAD_FAST                'mask'
              158  STORE_SUBSCR     

 L. 288       160  LOAD_FAST                'x1'
              162  LOAD_CONST               1
              164  BINARY_SUBSCR    
              166  LOAD_FAST                'x1'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  BINARY_SUBTRACT  
              174  LOAD_FAST                'denom'
              176  BINARY_TRUE_DIVIDE
              178  STORE_FAST               's'

 L. 289       180  LOAD_CONST               1.0
              182  LOAD_FAST                's'
              184  LOAD_FAST                'mask'
              186  STORE_SUBSCR     

 L. 290       188  LOAD_CONST               1.0
              190  LOAD_FAST                's'
              192  LOAD_FAST                'x0'
              194  LOAD_CONST               1
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'x0'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  COMPARE_OP               ==
              206  STORE_SUBSCR     

 L. 291       208  LOAD_FAST                'x1'
              210  LOAD_CONST               0
              212  BINARY_SUBSCR    
              214  LOAD_FAST                's'
              216  LOAD_FAST                'x0'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  BINARY_MULTIPLY  
              224  BINARY_SUBTRACT  
              226  STORE_FAST               't'

 L. 292       228  LOAD_GLOBAL              as_vec4
              230  LOAD_FAST                's'
              232  LOAD_CONST               (1, 1, 1, 1)
              234  LOAD_CONST               ('default',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  STORE_FAST               's'

 L. 293       240  LOAD_GLOBAL              as_vec4
              242  LOAD_FAST                't'
              244  LOAD_CONST               (0, 0, 0, 0)
              246  LOAD_CONST               ('default',)
              248  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              250  STORE_FAST               't'

 L. 294       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _set_st
              256  LOAD_FAST                's'
              258  LOAD_FAST                't'
              260  LOAD_FAST                'update'
              262  LOAD_CONST               ('scale', 'translate', 'update')
              264  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              266  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 128_0

    def __mul__(self, tr):
        if isinstance(tr, STTransform):
            s = self.scale * tr.scale
            t = self.translate + tr.translate * self.scale
            return STTransform(scale=s, translate=t)
        if isinstance(tr, MatrixTransform):
            return self.as_matrix() * tr
        return super(STTransform, self).__mul__(tr)

    def __rmul__(self, tr):
        if isinstance(tr, MatrixTransform):
            return tr * self.as_matrix()
        return super(STTransform, self).__rmul__(tr)

    def __repr__(self):
        return '<STTransform scale=%s translate=%s at 0x%s>' % (
         self.scale, self.translate, id(self))


class MatrixTransform(BaseTransform):
    __doc__ = 'Affine transformation class\n\n    Parameters\n    ----------\n    matrix : array-like | None\n        4x4 array to use for the transform.\n    '
    glsl_map = '\n        vec4 affine_transform_map(vec4 pos) {\n            return $matrix * pos;\n        }\n    '
    glsl_imap = '\n        vec4 affine_transform_imap(vec4 pos) {\n            return $inv_matrix * pos;\n        }\n    '
    Linear = True
    Orthogonal = False
    NonScaling = False
    Isometric = False

    def __init__(self, matrix=None):
        super(MatrixTransform, self).__init__()
        if matrix is not None:
            self.matrix = matrix
        else:
            self.reset()

    @arg_to_vec4
    def map(self, coords):
        """Map coordinates

        Parameters
        ----------
        coords : array-like
            Coordinates to map.

        Returns
        -------
        coords : ndarray
            Coordinates.
        """
        return np.dot(coords, self.matrix)

    @arg_to_vec4
    def imap(self, coords):
        """Inverse map coordinates

        Parameters
        ----------
        coords : array-like
            Coordinates to inverse map.

        Returns
        -------
        coords : ndarray
            Coordinates.
        """
        return np.dot(coords, self.inv_matrix)

    def shader_map(self):
        fn = super(MatrixTransform, self).shader_map()
        fn['matrix'] = self.matrix
        return fn

    def shader_imap(self):
        fn = super(MatrixTransform, self).shader_imap()
        fn['inv_matrix'] = self.inv_matrix
        return fn

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, m):
        self._matrix = m
        self._inv_matrix = None
        self.shader_map()
        self.shader_imap()
        self.update()

    @property
    def inv_matrix(self):
        if self._inv_matrix is None:
            self._inv_matrix = np.linalg.inv(self.matrix)
        return self._inv_matrix

    @arg_to_vec4
    def translate(self, pos):
        """
        Translate the matrix

        The translation is applied *after* the transformations already present
        in the matrix.

        Parameters
        ----------
        pos : arrayndarray
            Position to translate by.
        """
        self.matrix = np.dot(self.matrix, transforms.translate(pos[0, :3]))

    def scale(self, scale, center=None):
        """
        Scale the matrix about a given origin.

        The scaling is applied *after* the transformations already present
        in the matrix.

        Parameters
        ----------
        scale : array-like
            Scale factors along x, y and z axes.
        center : array-like or None
            The x, y and z coordinates to scale around. If None,
            (0, 0, 0) will be used.
        """
        scale = transforms.scale(as_vec4(scale, default=(1, 1, 1, 1))[0, :3])
        if center is not None:
            center = as_vec4(center)[0, :3]
            scale = np.dot(np.dot(transforms.translate(-center), scale), transforms.translate(center))
        self.matrix = np.dot(self.matrix, scale)

    def rotate(self, angle, axis):
        """
        Rotate the matrix by some angle about a given axis.

        The rotation is applied *after* the transformations already present
        in the matrix.

        Parameters
        ----------
        angle : float
            The angle of rotation, in degrees.
        axis : array-like
            The x, y and z coordinates of the axis vector to rotate around.
        """
        self.matrix = np.dot(self.matrix, transforms.rotate(angle, axis))

    def set_mapping(self, points1, points2):
        """ Set to a 3D transformation matrix that maps points1 onto points2.

        Parameters
        ----------
        points1 : array-like, shape (4, 3)
            Four starting 3D coordinates.
        points2 : array-like, shape (4, 3)
            Four ending 3D coordinates.
        """
        self.matrix = transforms.affine_map(points1, points2).T

    def set_ortho(self, l, r, b, t, n, f):
        """Set ortho transform

        Parameters
        ----------
        l : float
            Left.
        r : float
            Right.
        b : float
            Bottom.
        t : float
            Top.
        n : float
            Near.
        f : float
            Far.
        """
        self.matrix = transforms.ortho(l, r, b, t, n, f)

    def reset(self):
        self.matrix = np.eye(4)

    def __mul__(self, tr):
        if isinstance(tr, MatrixTransform):
            if not any(tr.matrix[:3, 3] != 0):
                return MatrixTransform(matrix=(np.dot(tr.matrix, self.matrix)))
        return tr.__rmul__(self)

    def __repr__(self):
        s = '%s(matrix=[' % self.__class__.__name__
        indent = ' ' * len(s)
        s += str(list(self.matrix[0])) + ',\n'
        s += indent + str(list(self.matrix[1])) + ',\n'
        s += indent + str(list(self.matrix[2])) + ',\n'
        s += indent + str(list(self.matrix[3])) + '] at 0x%x)' % id(self)
        return s

    def set_perspective(self, fov, aspect, near, far):
        """Set the perspective

        Parameters
        ----------
        fov : float
            Field of view.
        aspect : float
            Aspect ratio.
        near : float
            Near location.
        far : float
            Far location.
        """
        self.matrix = transforms.perspective(fov, aspect, near, far)

    def set_frustum(self, l, r, b, t, n, f):
        """Set the frustum

        Parameters
        ----------
        l : float
            Left.
        r : float
            Right.
        b : float
            Bottom.
        t : float
            Top.
        n : float
            Near.
        f : float
            Far.
        """
        self.matrix = transforms.frustum(l, r, b, t, n, f)