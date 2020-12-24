# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/image.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 15671 bytes
from __future__ import division
import numpy as np
from ..gloo import Texture2D, VertexBuffer
from ..color import get_colormap
from .shaders import Function, FunctionChain
from .transforms import NullTransform
from .visual import Visual
from ext.six import string_types
from ..io import load_spatial_filters
VERT_SHADER = '\nuniform int method;  // 0=subdivide, 1=impostor\nattribute vec2 a_position;\nattribute vec2 a_texcoord;\nvarying vec2 v_texcoord;\n\nvoid main() {\n    v_texcoord = a_texcoord;\n    gl_Position = $transform(vec4(a_position, 0., 1.));\n}\n'
FRAG_SHADER = '\nuniform vec2 image_size;\nuniform int method;  // 0=subdivide, 1=impostor\nuniform sampler2D u_texture;\nvarying vec2 v_texcoord;\n\nvec4 map_local_to_tex(vec4 x) {\n    // Cast ray from 3D viewport to surface of image\n    // (if $transform does not affect z values, then this\n    // can be optimized as simply $transform.map(x) )\n    vec4 p1 = $transform(x);\n    vec4 p2 = $transform(x + vec4(0, 0, 0.5, 0));\n    p1 /= p1.w;\n    p2 /= p2.w;\n    vec4 d = p2 - p1;\n    float f = p2.z / d.z;\n    vec4 p3 = p2 - d * f;\n    \n    // finally map local to texture coords\n    return vec4(p3.xy / image_size, 0, 1);\n}\n\n\nvoid main()\n{\n    vec2 texcoord;\n    if( method == 0 ) {\n        texcoord = v_texcoord;\n    }\n    else {\n        // vertex shader ouptuts clip coordinates; \n        // fragment shader maps to texture coordinates\n        texcoord = map_local_to_tex(vec4(v_texcoord, 0, 1)).xy;\n    }\n    \n    gl_FragColor = $color_transform($get_data(texcoord));\n}\n'
_null_color_transform = 'vec4 pass(vec4 color) { return color; }'
_c2l = 'float cmap(vec4 color) { return (color.r + color.g + color.b) / 3.; }'
_interpolation_template = '\n    #include "misc/spatial-filters.frag"\n    vec4 texture_lookup_filtered(vec2 texcoord) {\n        if(texcoord.x < 0.0 || texcoord.x > 1.0 ||\n        texcoord.y < 0.0 || texcoord.y > 1.0) {\n            discard;\n        }\n        return %s($texture, $shape, texcoord);\n    }'
_texture_lookup = '\n    vec4 texture_lookup(vec2 texcoord) {\n        if(texcoord.x < 0.0 || texcoord.x > 1.0 ||\n        texcoord.y < 0.0 || texcoord.y > 1.0) {\n            discard;\n        }\n        return texture2D($texture, texcoord);\n    }'

class ImageVisual(Visual):
    __doc__ = "Visual subclass displaying an image.\n\n    Parameters\n    ----------\n    data : ndarray\n        ImageVisual data. Can be shape (M, N), (M, N, 3), or (M, N, 4).\n    method : str\n        Selects method of rendering image in case of non-linear transforms.\n        Each method produces similar results, but may trade efficiency\n        and accuracy. If the transform is linear, this parameter is ignored\n        and a single quad is drawn around the area of the image.\n\n            * 'auto': Automatically select 'impostor' if the image is drawn\n              with a nonlinear transform; otherwise select 'subdivide'.\n            * 'subdivide': ImageVisual is represented as a grid of triangles\n              with texture coordinates linearly mapped.\n            * 'impostor': ImageVisual is represented as a quad covering the\n              entire view, with texture coordinates determined by the\n              transform. This produces the best transformation results, but may\n              be slow.\n\n    grid: tuple (rows, cols)\n        If method='subdivide', this tuple determines the number of rows and\n        columns in the image grid.\n    cmap : str | ColorMap\n        Colormap to use for luminance images.\n    clim : str | tuple\n        Limits to use for the colormap. Can be 'auto' to auto-set bounds to\n        the min and max of the data.\n    interpolation : str\n        Selects method of image interpolation. Makes use of the two Texture2D\n        interpolation methods and the available interpolation methods defined\n        in vispy/gloo/glsl/misc/spatial_filters.frag\n\n            * 'nearest': Default, uses 'nearest' with Texture2D interpolation.\n            * 'bilinear': uses 'linear' with Texture2D interpolation.\n            * 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'bicubic',\n                'catrom', 'mitchell', 'spline16', 'spline36', 'gaussian',\n                'bessel', 'sinc', 'lanczos', 'blackman'\n\n    **kwargs : dict\n        Keyword arguments to pass to `Visual`.\n\n    Notes\n    -----\n    The colormap functionality through ``cmap`` and ``clim`` are only used\n    if the data are 2D.\n    "

    def __init__(self, data=None, method='auto', grid=(1, 1), cmap='viridis', clim='auto', interpolation='nearest', **kwargs):
        self._data = None
        kernel, self._interpolation_names = load_spatial_filters()
        self._kerneltex = Texture2D(kernel, interpolation='nearest')
        fun = [Function(_interpolation_template % n) for n in self._interpolation_names]
        self._interpolation_names = [n.lower() for n in self._interpolation_names]
        self._interpolation_fun = dict(zip(self._interpolation_names, fun))
        self._interpolation_names.sort()
        self._interpolation_names = tuple(self._interpolation_names)
        self._interpolation_fun['nearest'] = Function(_texture_lookup)
        self._interpolation_fun['bilinear'] = Function(_texture_lookup)
        if interpolation not in self._interpolation_names:
            raise ValueError('interpolation must be one of %s' % ', '.join(self._interpolation_names))
        else:
            self._interpolation = interpolation
            if self._interpolation == 'bilinear':
                texture_interpolation = 'linear'
            else:
                texture_interpolation = 'nearest'
        self._method = method
        self._grid = grid
        self._need_texture_upload = True
        self._need_vertex_update = True
        self._need_colortransform_update = True
        self._need_interpolation_update = True
        self._texture = Texture2D((np.zeros((1, 1, 4))), interpolation=texture_interpolation)
        self._subdiv_position = VertexBuffer()
        self._subdiv_texcoord = VertexBuffer()
        vertices = np.array([[-1, -1], [1, -1], [1, 1],
         [
          -1, -1], [1, 1], [-1, 1]],
          dtype=(np.float32))
        self._impostor_coords = VertexBuffer(vertices)
        self._null_tr = NullTransform()
        self._init_view(self)
        super(ImageVisual, self).__init__(vcode=VERT_SHADER, fcode=FRAG_SHADER)
        self.set_gl_state('translucent', cull_face=False)
        self._draw_mode = 'triangles'
        self._data_lookup_fn = None
        self.clim = clim
        self.cmap = cmap
        if data is not None:
            self.set_data(data)
        self.freeze()

    def set_data(self, image):
        """Set the data

        Parameters
        ----------
        image : array-like
            The image data.
        """
        data = np.asarray(image)
        if self._data is None or self._data.shape != data.shape:
            self._need_vertex_update = True
        self._data = data
        self._need_texture_upload = True

    def view(self):
        v = Visual.view(self)
        self._init_view(v)
        return v

    def _init_view(self, view):
        view._need_method_update = True
        view._method_used = None

    @property
    def clim(self):
        if isinstance(self._clim, string_types):
            return self._clim
        return tuple(self._clim)

    @clim.setter
    def clim(self, clim):
        if isinstance(clim, string_types):
            if clim != 'auto':
                raise ValueError('clim must be "auto" if a string')
        else:
            clim = np.array(clim, float)
            if clim.shape != (2, ):
                raise ValueError('clim must have two elements')
        self._clim = clim
        self._need_texture_upload = True
        self.update()

    @property
    def cmap(self):
        return self._cmap

    @cmap.setter
    def cmap(self, cmap):
        self._cmap = get_colormap(cmap)
        self._need_colortransform_update = True
        self.update()

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, m):
        if self._method != m:
            self._method = m
            self._need_vertex_update = True
            self.update()

    @property
    def size(self):
        return self._data.shape[:2][::-1]

    @property
    def interpolation(self):
        return self._interpolation

    @interpolation.setter
    def interpolation(self, i):
        if i not in self._interpolation_names:
            raise ValueError('interpolation must be one of %s' % ', '.join(self._interpolation_names))
        if self._interpolation != i:
            self._interpolation = i
            self._need_interpolation_update = True
            self.update()

    @property
    def interpolation_functions(self):
        return self._interpolation_names

    def _build_interpolation(self):
        """Rebuild the _data_lookup_fn using different interpolations within
        the shader
        """
        interpolation = self._interpolation
        self._data_lookup_fn = self._interpolation_fun[interpolation]
        self.shared_program.frag['get_data'] = self._data_lookup_fn
        if interpolation == 'bilinear':
            texture_interpolation = 'linear'
        else:
            texture_interpolation = 'nearest'
            if interpolation != 'nearest':
                self.shared_program['u_kernel'] = self._kerneltex
                self._data_lookup_fn['shape'] = self._data.shape[:2][::-1]
        if self._texture.interpolation != texture_interpolation:
            self._texture.interpolation = texture_interpolation
        self._data_lookup_fn['texture'] = self._texture
        self._need_interpolation_update = False

    def _build_vertex_data(self):
        """Rebuild the vertex buffers used for rendering the image when using
        the subdivide method.
        """
        grid = self._grid
        w = 1.0 / grid[1]
        h = 1.0 / grid[0]
        quad = np.array([[0, 0, 0], [w, 0, 0], [w, h, 0],
         [
          0, 0, 0], [w, h, 0], [0, h, 0]],
          dtype=(np.float32))
        quads = np.empty((grid[1], grid[0], 6, 3), dtype=(np.float32))
        quads[:] = quad
        mgrid = np.mgrid[0.0:grid[1], 0.0:grid[0]].transpose(1, 2, 0)
        mgrid = mgrid[:, :, np.newaxis, :]
        mgrid[(Ellipsis, 0)] *= w
        mgrid[(Ellipsis, 1)] *= h
        quads[..., :2] += mgrid
        tex_coords = quads.reshape(grid[1] * grid[0] * 6, 3)
        tex_coords = np.ascontiguousarray(tex_coords[:, :2])
        vertices = tex_coords * self.size
        self._subdiv_position.set_data(vertices.astype('float32'))
        self._subdiv_texcoord.set_data(tex_coords.astype('float32'))

    def _update_method(self, view):
        """Decide which method to use for *view* and configure it accordingly.
        """
        method = self._method
        if method == 'auto':
            if view.transforms.get_transform().Linear:
                method = 'subdivide'
            else:
                method = 'impostor'
        else:
            view._method_used = method
            if method == 'subdivide':
                view.view_program['method'] = 0
                view.view_program['a_position'] = self._subdiv_position
                view.view_program['a_texcoord'] = self._subdiv_texcoord
            else:
                if method == 'impostor':
                    view.view_program['method'] = 1
                    view.view_program['a_position'] = self._impostor_coords
                    view.view_program['a_texcoord'] = self._impostor_coords
                else:
                    raise ValueError("Unknown image draw method '%s'" % method)
        self.shared_program['image_size'] = self.size
        view._need_method_update = False
        self._prepare_transforms(view)

    def _build_color_transform(self):
        data = self._data
        if data.ndim == 2 or data.shape[2] == 1:
            fun = FunctionChain(None, [Function(_c2l),
             Function(self._cmap.glsl_map)])
        else:
            fun = Function(_null_color_transform)
        self.shared_program.frag['color_transform'] = fun
        self._need_colortransform_update = False

    def _build_texture(self):
        data = self._data
        if data.dtype == np.float64:
            data = data.astype(np.float32)
        if data.ndim == 2 or data.shape[2] == 1:
            clim = self._clim
            if isinstance(clim, string_types):
                if clim == 'auto':
                    clim = (
                     np.min(data), np.max(data))
            else:
                clim = np.asarray(clim, dtype=(np.float32))
                data = data - clim[0]
                if clim[1] - clim[0] > 0:
                    data /= clim[1] - clim[0]
                else:
                    data[:] = 1 if data[(0, 0)] != 0 else 0
            self._clim = np.array(clim)
        self._texture.set_data(data)
        self._need_texture_upload = False

    def _compute_bounds(self, axis, view):
        if axis > 1:
            return (0, 0)
        return (0, self.size[axis])

    def _prepare_transforms(self, view):
        trs = view.transforms
        prg = view.view_program
        method = view._method_used
        if method == 'subdivide':
            prg.vert['transform'] = trs.get_transform()
            prg.frag['transform'] = self._null_tr
        else:
            prg.vert['transform'] = self._null_tr
            prg.frag['transform'] = trs.get_transform().inverse

    def _prepare_draw(self, view):
        if self._data is None:
            return False
        if self._need_interpolation_update:
            self._build_interpolation()
        if self._need_texture_upload:
            self._build_texture()
        if self._need_colortransform_update:
            self._build_color_transform()
        if self._need_vertex_update:
            self._build_vertex_data()
        if view._need_method_update:
            self._update_method(view)