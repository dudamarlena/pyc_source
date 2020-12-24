# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/transforms/nonlinear.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 12712 bytes
from __future__ import division
import numpy as np
from ._util import arg_to_array, arg_to_vec4, as_vec4
from .base_transform import BaseTransform
from ... import gloo

class LogTransform(BaseTransform):
    __doc__ = ' Transform perfoming logarithmic transformation on three axes.\n\n    Maps (x, y, z) => (log(base.x, x), log(base.y, y), log(base.z, z))\n\n    No transformation is applied for axes with base == 0.\n\n    If base < 0, then the inverse function is applied: x => base.x ** x\n\n    Parameters\n    ----------\n    base : array-like\n        Base for the X, Y, Z axes.\n    '
    glsl_map = '\n        vec4 LogTransform_map(vec4 pos) {\n            if($base.x > 1.0)\n                pos.x = log(pos.x) / log($base.x);\n            else if($base.x < -1.0)\n                pos.x = pow(-$base.x, pos.x);\n\n            if($base.y > 1.0)\n                pos.y = log(pos.y) / log($base.y);\n            else if($base.y < -1.0)\n                pos.y = pow(-$base.y, pos.y);\n\n            if($base.z > 1.0)\n                pos.z = log(pos.z) / log($base.z);\n            else if($base.z < -1.0)\n                pos.z = pow(-$base.z, pos.z);\n            return pos;\n        }\n        '
    glsl_imap = glsl_map
    Linear = False
    Orthogonal = True
    NonScaling = False
    Isometric = False

    def __init__(self, base=None):
        super(LogTransform, self).__init__()
        self._base = np.zeros(3, dtype=np.float32)
        self.base = (0.0, 0.0, 0.0) if base is None else base

    @property
    def base(self):
        """
        *base* is a tuple (x, y, z) containing the log base that should be
        applied to each axis of the input vector. If any axis has a base <= 0,
        then that axis is not affected.
        """
        return self._base.copy()

    @base.setter
    def base(self, s):
        self._base[:len(s)] = s
        self._base[len(s):] = 0.0

    @arg_to_array
    def map(self, coords, base=None):
        ret = np.empty(coords.shape, coords.dtype)
        if base is None:
            base = self.base
        for i in range(min(ret.shape[(-1)], 3)):
            if base[i] > 1.0:
                ret[(..., i)] = np.log(coords[(..., i)]) / np.log(base[i])
            else:
                if base[i] < -1.0:
                    ret[(..., i)] = -base[i] ** coords[(..., i)]
                else:
                    ret[(..., i)] = coords[(..., i)]

        return ret

    @arg_to_array
    def imap(self, coords):
        return self.map(coords, -self.base)

    def shader_map(self):
        fn = super(LogTransform, self).shader_map()
        fn['base'] = self.base
        return fn

    def shader_imap(self):
        fn = super(LogTransform, self).shader_imap()
        fn['base'] = -self.base
        return fn

    def __repr__(self):
        return '<LogTransform base=%s>' % self.base


class PolarTransform(BaseTransform):
    __doc__ = 'Polar transform\n\n    Maps (theta, r, z) to (x, y, z), where `x = r*cos(theta)`\n    and `y = r*sin(theta)`.\n    '
    glsl_map = '\n        vec4 polar_transform_map(vec4 pos) {\n            return vec4(pos.y * cos(pos.x), pos.y * sin(pos.x), pos.z, 1);\n        }\n        '
    glsl_imap = '\n        vec4 polar_transform_map(vec4 pos) {\n            // TODO: need some modulo math to handle larger theta values..?\n            float theta = atan(pos.y, pos.x);\n            float r = length(pos.xy);\n            return vec4(theta, r, pos.z, 1);\n        }\n        '
    Linear = False
    Orthogonal = False
    NonScaling = False
    Isometric = False

    @arg_to_array
    def map(self, coords):
        ret = np.empty(coords.shape, coords.dtype)
        ret[(Ellipsis, 0)] = coords[(Ellipsis, 1)] * np.cos(coords[(Ellipsis, 0)])
        ret[(Ellipsis, 1)] = coords[(Ellipsis, 1)] * np.sin(coords[(Ellipsis, 0)])
        for i in range(2, coords.shape[(-1)]):
            ret[(..., i)] = coords[(..., i)]

        return ret

    @arg_to_array
    def imap(self, coords):
        ret = np.empty(coords.shape, coords.dtype)
        ret[(Ellipsis, 0)] = np.arctan2(coords[(Ellipsis, 0)], coords[(Ellipsis, 1)])
        ret[(Ellipsis, 1)] = (coords[(Ellipsis, 0)] ** 2 + coords[(Ellipsis, 1)] ** 2) ** 0.5
        for i in range(2, coords.shape[(-1)]):
            ret[(..., i)] = coords[(..., i)]

        return ret


class MagnifyTransform(BaseTransform):
    __doc__ = ' Magnifying lens transform. \n\n    This transform causes a circular region to appear with larger scale around\n    its center point. \n    \n    Parameters\n    ----------\n    mag : float\n        Magnification factor. Objects around the transform\'s center point will\n        appear scaled by this amount relative to objects outside the circle.\n    radii : (float, float)\n        Inner and outer radii of the "lens". Objects inside the inner radius\n        appear scaled, whereas objects outside the outer radius are unscaled,\n        and the scale factor transitions smoothly between the two radii.\n    center: (float, float)\n        The center (x, y) point of the "lens".\n        \n    Notes\n    -----\n    \n    This transform works by segmenting its input coordinates into three\n    regions--inner, outer, and transition. Coordinates in the inner region are\n    multiplied by a constant scale factor around the center point, and \n    coordinates in the transition region are scaled by a factor that \n    transitions smoothly from the inner radius to the outer radius. \n    \n    Smooth functions that are appropriate for the transition region also tend \n    to be difficult to invert analytically, so this transform instead samples\n    the function numerically to allow trivial inversion. In OpenGL, the \n    sampling is implemented as a texture holding a lookup table.\n    '
    glsl_map = '\n        vec4 mag_transform(vec4 pos) {\n            vec2 d = vec2(pos.x - $center.x, pos.y - $center.y);\n            float dist = length(d);\n            if (dist == 0 || dist > $radii.y || ($mag < 1.01 && $mag > 0.99)) {\n                return pos;\n            }\n            vec2 dir = d / dist;\n            \n            if( dist < $radii.x ) {\n                dist = dist * $mag;\n            }\n            else {\n                \n                float r1 = $radii.x;\n                float r2 = $radii.y;\n                float x = (dist - r1) / (r2 - r1);\n                float s = texture2D($trans, vec2(0, x)).r * $trans_max;\n                \n                dist = s;\n            }\n\n            d = $center + dir * dist;\n            return vec4(d, pos.z, pos.w);\n        }'
    glsl_imap = glsl_map
    Linear = False
    _trans_resolution = 1000

    def __init__(self, mag=3, radii=(7, 10), center=(0, 0)):
        self._center = center
        self._mag = mag
        self._radii = radii
        self._trans = None
        res = self._trans_resolution
        self._trans_tex = (gloo.Texture2D((res, 1, 1), interpolation='linear'),
         gloo.Texture2D((res, 1, 1), interpolation='linear'))
        self._trans_tex_max = None
        super(MagnifyTransform, self).__init__()

    @property
    def center(self):
        """ The (x, y) center point of the transform.
        """
        return self._center

    @center.setter
    def center(self, center):
        if np.allclose(self._center, center):
            return
        self._center = center
        self.shader_map()
        self.shader_imap()

    @property
    def mag(self):
        """ The scale factor used in the central region of the transform.
        """
        return self._mag

    @mag.setter
    def mag(self, mag):
        if self._mag == mag:
            return
        self._mag = mag
        self._trans = None
        self.shader_map()
        self.shader_imap()

    @property
    def radii(self):
        """ The inner and outer radii of the circular area bounding the 
        transform.
        """
        return self._radii

    @radii.setter
    def radii(self, radii):
        if np.allclose(self._radii, radii):
            return
        self._radii = radii
        self._trans = None
        self.shader_map()
        self.shader_imap()

    def shader_map(self):
        fn = super(MagnifyTransform, self).shader_map()
        fn['center'] = self._center
        fn['mag'] = self._mag
        fn['radii'] = (self._radii[0] / self._mag, self._radii[1])
        self._get_transition()
        fn['trans'] = self._trans_tex[0]
        fn['trans_max'] = self._trans_tex_max[0]
        return fn

    def shader_imap(self):
        fn = super(MagnifyTransform, self).shader_imap()
        fn['center'] = self._center
        fn['mag'] = 1.0 / self._mag
        fn['radii'] = self._radii
        self._get_transition()
        fn['trans'] = self._trans_tex[1]
        fn['trans_max'] = self._trans_tex_max[1]
        return fn

    @arg_to_vec4
    def map(self, x, _inverse=False):
        c = as_vec4(self.center)[0]
        m = self.mag
        r1, r2 = self.radii
        xm = np.empty(x.shape, dtype=x.dtype)
        dx = x - c
        dist = ((dx ** 2).sum(axis=-1) ** 0.5)[(..., np.newaxis)]
        dist[np.isnan(dist)] = 0
        unit = dx / dist
        if _inverse:
            inner = (dist < r1)[:, 0]
            s = dist / m
        else:
            inner = (dist < r1 / m)[:, 0]
            s = dist * m
        xm[inner] = c + unit[inner] * s[inner]
        outer = (dist > r2)[:, 0]
        xm[outer] = x[outer]
        trans = ~(inner | outer)
        temp, itemp = self._get_transition()
        if _inverse:
            tind = (dist[trans] - r1) * len(itemp) / (r2 - r1)
            temp = itemp
        else:
            tind = (dist[trans] - r1 / m) * len(temp) / (r2 - r1 / m)
        tind = np.clip(tind, 0, temp.shape[0] - 1)
        s = temp[tind.astype(int)]
        xm[trans] = c + unit[trans] * s
        return xm

    def imap(self, coords):
        return self.map(coords, _inverse=True)

    def _get_transition(self):
        if self._trans is None:
            m, r1, r2 = self.mag, self.radii[0], self.radii[1]
            res = self._trans_resolution
            xi = np.linspace(r1, r2, res)
            t = 0.5 * (1 + np.cos((xi - r2) * np.pi / (r2 - r1)))
            yi = (xi * t + xi * (1 - t) / m).astype(np.float32)
            x = np.linspace(r1 / m, r2, res)
            y = np.interp(x, yi, xi).astype(np.float32)
            self._trans = (
             y, yi)
            mx = (
             y.max(), yi.max())
            self._trans_tex_max = mx
            self._trans_tex[0].set_data((y / mx[0])[:, np.newaxis, np.newaxis])
            self._trans_tex[1].set_data((yi / mx[1])[:, np.newaxis, np.newaxis])
        return self._trans


class Magnify1DTransform(MagnifyTransform):
    __doc__ = ' A 1-dimensional analog of MagnifyTransform. This transform expands \n    its input along the x-axis, around a center x value.\n    '
    glsl_map = '\n        vec4 mag_transform(vec4 pos) {\n            float dist = pos.x - $center.x;\n            if (dist == 0 || abs(dist) > $radii.y || $mag == 1) {\n                return pos;\n            }\n            float dir = dist / abs(dist);\n            \n            if( abs(dist) < $radii.x ) {\n                dist = dist * $mag;\n            }\n            else {\n                float r1 = $radii.x;\n                float r2 = $radii.y;\n                float x = (abs(dist) - r1) / (r2 - r1);\n                dist = dir * texture2D($trans, vec2(0, x)).r * $trans_max;\n            }\n\n            return vec4($center.x + dist, pos.y, pos.z, pos.w);\n        }'
    glsl_imap = glsl_map