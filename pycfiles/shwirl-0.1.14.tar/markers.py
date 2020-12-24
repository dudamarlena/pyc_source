# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/markers.py
# Compiled at: 2016-11-03 01:40:19
"""
Marker Visual and shader definitions.
"""
import numpy as np
from ..color import ColorArray
from ..gloo import VertexBuffer, _check_valid
from .shaders import Function, Variable
from .visual import Visual
vert = '\nuniform float u_antialias;\nuniform float u_px_scale;\nuniform float u_scale;\n\nattribute vec3  a_position;\nattribute vec4  a_fg_color;\nattribute vec4  a_bg_color;\nattribute float a_edgewidth;\nattribute float a_size;\n\nvarying vec4 v_fg_color;\nvarying vec4 v_bg_color;\nvarying float v_edgewidth;\nvarying float v_antialias;\n\nvoid main (void) {\n    $v_size = a_size * u_px_scale * u_scale;\n    v_edgewidth = a_edgewidth * u_px_scale;\n    v_antialias = u_antialias;\n    v_fg_color  = a_fg_color;\n    v_bg_color  = a_bg_color;\n    gl_Position = $transform(vec4(a_position,1.0));\n    float edgewidth = max(v_edgewidth, 1.0);\n    gl_PointSize = $v_size + 4*(edgewidth + 1.5*v_antialias);\n}\n'
frag = '\nvarying vec4 v_fg_color;\nvarying vec4 v_bg_color;\nvarying float v_edgewidth;\nvarying float v_antialias;\n\nvoid main()\n{\n    float edgewidth = max(v_edgewidth, 1.0);\n    float edgealphafactor = min(v_edgewidth, 1.0);\n\n    float size = $v_size + 4*(edgewidth + 1.5*v_antialias);\n    // factor 6 for acute edge angles that need room as for star marker\n\n    // The marker function needs to be linked with this shader\n    float r = $marker(gl_PointCoord, size);\n\n    // it takes into account an antialising layer\n    // of size v_antialias inside the edge\n    // r:\n    // [-e/2-a, -e/2+a] antialising face-edge\n    // [-e/2+a, e/2-a] core edge (center 0, diameter e-2a = 2t)\n    // [e/2-a, e/2+a] antialising edge-background\n    float t = 0.5*v_edgewidth - v_antialias;\n    float d = abs(r) - t;\n\n    vec4 edgecolor = vec4(v_fg_color.rgb, edgealphafactor*v_fg_color.a);\n\n    if (r > 0.5*v_edgewidth + v_antialias)\n    {\n        // out of the marker (beyond the outer edge of the edge\n        // including transition zone due to antialiasing)\n        discard;\n    }\n    else if (d < 0.0)\n    {\n        // inside the width of the edge\n        // (core, out of the transition zone for antialiasing)\n        gl_FragColor = edgecolor;\n    }\n    else\n    {\n        if (v_edgewidth == 0.)\n        {// no edge\n            if (r > -v_antialias)\n            {\n                float alpha = 1.0 + r/v_antialias;\n                alpha = exp(-alpha*alpha);\n                gl_FragColor = vec4(v_bg_color.rgb, alpha*v_bg_color.a);\n            }\n            else\n            {\n                gl_FragColor = v_bg_color;\n            }\n        }\n        else\n        {\n            float alpha = d/v_antialias;\n            alpha = exp(-alpha*alpha);\n            if (r > 0)\n            {\n                // outer part of the edge: fade out into the background...\n                gl_FragColor = vec4(edgecolor.rgb, alpha*edgecolor.a);\n            }\n            else\n            {\n                gl_FragColor = mix(v_bg_color, edgecolor, alpha);\n            }\n        }\n    }\n}\n'
disc = '\nfloat disc(vec2 pointcoord, float size)\n{\n    float r = length((pointcoord.xy - vec2(0.5,0.5))*size);\n    r -= $v_size/2;\n    return r;\n}\n'
arrow = '\nconst float sqrt2 = sqrt(2.);\nfloat rect(vec2 pointcoord, float size)\n{\n    float half_size = $v_size/2.;\n    float ady = abs(pointcoord.y -.5)*size;\n    float dx = (pointcoord.x -.5)*size;\n    float r1 = abs(dx) + ady - half_size;\n    float r2 = dx + 0.25*$v_size + ady - half_size;\n    float r = max(r1,-r2);\n    return r/sqrt2;//account for slanted edge and correct for width\n}\n'
ring = '\nfloat ring(vec2 pointcoord, float size)\n{\n    float r1 = length((pointcoord.xy - vec2(0.5,0.5))*size) - $v_size/2;\n    float r2 = length((pointcoord.xy - vec2(0.5,0.5))*size) - $v_size/4;\n    float r = max(r1,-r2);\n    return r;\n}\n'
clobber = '\nconst float sqrt3 = sqrt(3.);\nfloat clobber(vec2 pointcoord, float size)\n{\n    const float PI = 3.14159265358979323846264;\n    const float t1 = -PI/2;\n    float circle_radius = 0.32 * $v_size;\n    float center_shift = 0.36/sqrt3 * $v_size;\n    //total size (horizontal) = 2*circle_radius + sqrt3*center_shirt = $v_size\n    vec2  c1 = vec2(cos(t1),sin(t1))*center_shift;\n    const float t2 = t1+2*PI/3;\n    vec2  c2 = vec2(cos(t2),sin(t2))*center_shift;\n    const float t3 = t2+2*PI/3;\n    vec2  c3 = vec2(cos(t3),sin(t3))*center_shift;\n    //xy is shift to center marker vertically\n    vec2 xy = (pointcoord.xy-vec2(0.5,0.5))*size + vec2(0.,-0.25*center_shift);\n    float r1 = length(xy - c1) - circle_radius;\n    float r2 = length(xy - c2) - circle_radius;\n    float r3 = length(xy - c3) - circle_radius;\n    float r = min(min(r1,r2),r3);\n    return r;\n}\n'
square = '\nfloat square(vec2 pointcoord, float size)\n{\n    float r = max(abs(pointcoord.x -.5)*size, abs(pointcoord.y -.5)*size);\n    r -= $v_size/2;\n    return r;\n}\n'
x_ = '\nfloat x_(vec2 pointcoord, float size)\n{\n    vec2 rotcoord = vec2((pointcoord.x + pointcoord.y - 1.) / sqrt(2.),\n                         (pointcoord.y - pointcoord.x) / sqrt(2.));\n    //vbar\n    float r1 = abs(rotcoord.x)*size - $v_size/6;\n    float r2 = abs(rotcoord.y)*size - $v_size/2;\n    float vbar = max(r1,r2);\n    //hbar\n    float r3 = abs(rotcoord.y)*size - $v_size/6;\n    float r4 = abs(rotcoord.x)*size - $v_size/2;\n    float hbar = max(r3,r4);\n    return min(vbar, hbar);\n}\n'
diamond = '\nfloat diamond(vec2 pointcoord, float size)\n{\n    float r = abs(pointcoord.x -.5)*size + abs(pointcoord.y -.5)*size;\n    r -= $v_size/2;\n    return r / sqrt(2.);//account for slanted edge and correct for width\n}\n'
vbar = '\nfloat vbar(vec2 pointcoord, float size)\n{\n    float r1 = abs(pointcoord.x - 0.5)*size - $v_size/6;\n    float r3 = abs(pointcoord.y - 0.5)*size - $v_size/2;\n    float r = max(r1,r3);\n    return r;\n}\n'
hbar = '\nfloat rect(vec2 pointcoord, float size)\n{\n    float r2 = abs(pointcoord.y - 0.5)*size - $v_size/6;\n    float r3 = abs(pointcoord.x - 0.5)*size - $v_size/2;\n    float r = max(r2,r3);\n    return r;\n}\n'
cross = '\nfloat cross(vec2 pointcoord, float size)\n{\n    //vbar\n    float r1 = abs(pointcoord.x - 0.5)*size - $v_size/6;\n    float r2 = abs(pointcoord.y - 0.5)*size - $v_size/2;\n    float vbar = max(r1,r2);\n    //hbar\n    float r3 = abs(pointcoord.y - 0.5)*size - $v_size/6;\n    float r4 = abs(pointcoord.x - 0.5)*size - $v_size/2;\n    float hbar = max(r3,r4);\n    return min(vbar, hbar);\n}\n'
tailed_arrow = '\nconst float sqrt2 = sqrt(2.);\nfloat rect(vec2 pointcoord, float size)\n{\n    float half_size = $v_size/2.;\n    float ady = abs(pointcoord.y -.5)*size;\n    float dx = (pointcoord.x -.5)*size;\n    float r1 = abs(dx) + ady - half_size;\n    float r2 = dx + 0.25*$v_size + ady - half_size;\n    float arrow = max(r1,-r2);\n    //hbar\n    float upper_bottom_edges = ady - $v_size/8./sqrt2;\n    float left_edge = -dx - half_size;\n    float right_edge = dx + ady - half_size;\n    float hbar = max(upper_bottom_edges, left_edge);\n    float scale = 1.; //rescaling for slanted edge\n    if (right_edge >= hbar)\n    {\n        hbar = right_edge;\n        scale = sqrt2;\n    }\n    if (arrow <= hbar)\n    {\n        return arrow / sqrt2;//account for slanted edge and correct for width\n    }\n    else\n    {\n        return hbar / scale;\n    }\n}\n'
triangle_up = '\nfloat rect(vec2 pointcoord, float size)\n{\n    float height = $v_size*sqrt(3.)/2.;\n    float bottom = ((pointcoord.y - 0.5)*size - height/2.);\n    float rotated_y = sqrt(3.)/2. * (pointcoord.x - 0.5) * size\n              - 0.5 * ((pointcoord.y - 0.5)*size - height/6.) + height/6.;\n    float right_edge = (rotated_y - height/2.);\n    float cc_rotated_y = -sqrt(3.)/2. * (pointcoord.x - 0.5)*size\n              - 0.5 * ((pointcoord.y - 0.5)*size - height/6.) + height/6.;\n    float left_edge = (cc_rotated_y - height/2.);\n    float slanted_edges = max(right_edge, left_edge);\n    return max(slanted_edges, bottom);\n}\n'
triangle_down = '\nfloat rect(vec2 pointcoord, float size)\n{\n    float height = -$v_size*sqrt(3.)/2.;\n    float bottom = -((pointcoord.y - 0.5)*size - height/2.);\n    float rotated_y = sqrt(3.)/2. * (pointcoord.x - 0.5) * size\n                - 0.5 * ((pointcoord.y - 0.5)*size - height/6.) + height/6.;\n    float right_edge = -(rotated_y - height/2.);\n    float cc_rotated_y = -sqrt(3.)/2. * (pointcoord.x - 0.5)*size\n                - 0.5 * ((pointcoord.y - 0.5)*size - height/6.) + height/6.;\n    float left_edge = -(cc_rotated_y - height/2.);\n    float slanted_edges = max(right_edge, left_edge);\n    return max(slanted_edges, bottom);\n}\n'
star = '\nfloat rect(vec2 pointcoord, float size)\n{\n    float star = -10000.;\n    const float PI2_5 = 3.141592653589*2./5.;\n    const float PI2_20 = 3.141592653589/10.;  //PI*2/20\n    // downwards shift to that the marker center is halfway vertically\n    // between the top of the upward spike (y = -v_size/2)\n    // and the bottom of one of two downward spikes\n    // (y = +v_size/2*cos(2*pi/10) approx +v_size/2*0.8)\n    // center is at -v_size/2*0.1\n    float shift_y = -0.05*$v_size;\n    // first spike upwards,\n    // rotate spike by 72 deg four times to complete the star\n    for (int i = 0; i <= 4; i++)\n    {\n        //if not the first spike, rotate it upwards\n        float x = (pointcoord.x - 0.5)*size;\n        float y = (pointcoord.y - 0.5)*size;\n        float spike_rot_angle = i*PI2_5;\n        float cosangle = cos(spike_rot_angle);\n        float sinangle = sin(spike_rot_angle);\n        float spike_x = x;\n        float spike_y = y + shift_y;\n        if (i > 0)\n        {\n            spike_x = cosangle * x - sinangle * (y + shift_y);\n            spike_y = sinangle * x + cosangle * (y + shift_y);\n        }\n        // in the frame where the spike is upwards:\n        // rotate 18 deg the zone x < 0 around the top of the star\n        // (point whose coords are -s/2, 0 where s is the size of the marker)\n        // compute y coordonates as well because\n        // we do a second rotation to put the spike at its final position\n        float rot_center_y = -$v_size/2;\n        float rot18x = cos(PI2_20) * spike_x\n                            - sin(PI2_20) * (spike_y - rot_center_y);\n        //rotate -18 deg the zone x > 0 arount the top of the star\n        float rot_18x = cos(PI2_20) * spike_x\n                            + sin(PI2_20) * (spike_y - rot_center_y);\n        float bottom = spike_y - $v_size/10.;\n        //                     max(left edge, right edge)\n        float spike = max(bottom, max(rot18x, -rot_18x));\n        if (i == 0)\n        {// first spike, skip the rotation\n            star = spike;\n        }\n        else // i > 0\n        {\n            star = min(star, spike);\n        }\n    }\n    return star;\n}\n'
rect = '\nfloat rect(vec2 pointcoord, float size)\n{\n    float x_boundaries = abs(pointcoord.x - 0.5)*size - $v_size.x/2.;\n    float y_boundaries = abs(pointcoord.y - 0.5)*size - $v_size.y/2.;\n    return max(x_boundaries, y_boundaries);\n}\n'
ellipse = "\nfloat rect(vec2 pointcoord, float size)\n{\n    float x = (pointcoord.x - 0.5)*size;\n    float y = (pointcoord.y - 0.5)*size;\n    // normalise radial distance (for edge and antialising to remain isotropic)\n    // Scaling factor is the norm of the gradient of the function defining\n    // the surface taken at a well chosen point on the edge of the ellipse\n    // f(x, y) = (sqrt(x^2/a^2 + y^2/b^2) = 0.5 in this case\n    // where a = v_size.x and b = v_size.y)\n    // The well chosen point on the edge of the ellipse should be the point\n    // whose normal points towards the current point.\n    // Below we choose a different point whose computation\n    // is simple enough to fit here.\n    float f = length(vec2(x / $v_size.x, y / $v_size.y));\n    // We set the default value of the norm so that\n    // - near the axes (x=0 or y=0 +/- 1 pixel), the norm is correct\n    //   (the computation below is unstable near the axes)\n    // - if the ellipse is a circle, the norm is correct\n    // - if we are deep in the interior of the ellipse the norm\n    //   is set to an arbitrary value (but is not used)\n    float norm = abs(x) < 1. ? 1./$v_size.y : 1./$v_size.x;\n    if (f > 1e-3 && abs($v_size.x - $v_size.y) > 1e-3\n        && abs(x) > 1. && abs(y) > 1.)\n    {\n        // Find the point x0, y0 on the ellipse which has the same hyperbola\n        // coordinate in the elliptic coordinate system linked to the ellipse\n        // (finding the right 'well chosen' point is too complicated)\n        // Visually it's nice, even at high eccentricities, where\n        // the approximation is visible but not ugly.\n        float a = $v_size.x/2.;\n        float b = $v_size.y/2.;\n        float C = max(a, b);\n        float c = min(a, b);\n        float focal_length = sqrt(C*C - c*c);\n        float fl2 = focal_length*focal_length;\n        float x2 = x*x;\n        float y2 = y*y;\n        float tmp = fl2 + x2 + y2;\n        float x0 = 0;\n        float y0 = 0;\n        if ($v_size.x > $v_size.y)\n        {\n            float cos2v = 0.5 * (tmp - sqrt(tmp*tmp - 4.*fl2*x2)) / fl2;\n            cos2v = fract(cos2v);\n            x0 = a * sqrt(cos2v);\n            // v_size.x = focal_length*cosh m where m is the ellipse coordinate\n            y0 = b * sqrt(1-cos2v);\n            // v_size.y = focal_length*sinh m\n        }\n        else // $v_size.x < $v_size.y\n        {//exchange x and y axis for elliptic coordinate\n            float cos2v = 0.5 * (tmp - sqrt(tmp*tmp - 4.*fl2*y2)) / fl2;\n            cos2v = fract(cos2v);\n            x0 = a * sqrt(1-cos2v);\n            // v_size.x = focal_length*sinh m where m is the ellipse coordinate\n            y0 = b * sqrt(cos2v);\n            // v_size.y = focal_length*cosh m\n        }\n        vec2 normal = vec2(2.*x0/v_size.x/v_size.x, 2.*y0/v_size.y/v_size.y);\n        norm = length(normal);\n    }\n    return (f - 0.5) / norm;\n}\n"
_marker_dict = {'disc': disc, 
   'arrow': arrow, 
   'ring': ring, 
   'clobber': clobber, 
   'square': square, 
   'diamond': diamond, 
   'vbar': vbar, 
   'hbar': hbar, 
   'cross': cross, 
   'tailed_arrow': tailed_arrow, 
   'x': x_, 
   'triangle_up': triangle_up, 
   'triangle_down': triangle_down, 
   'star': star, 
   'o': disc, 
   '+': cross, 
   's': square, 
   '-': hbar, 
   '|': vbar, 
   '->': tailed_arrow, 
   '>': arrow, 
   '^': triangle_up, 
   'v': triangle_down, 
   '*': star}
marker_types = tuple(sorted(list(_marker_dict.keys())))

class MarkersVisual(Visual):
    """ Visual displaying marker symbols.
    """

    def __init__(self, **kwargs):
        self._vbo = VertexBuffer()
        self._v_size_var = Variable('varying float v_size')
        self._symbol = None
        self._marker_fun = None
        self._data = None
        self.antialias = 1
        self.scaling = False
        Visual.__init__(self, vcode=vert, fcode=frag)
        self.shared_program.vert['v_size'] = self._v_size_var
        self.shared_program.frag['v_size'] = self._v_size_var
        self.set_gl_state(depth_test=True, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))
        self._draw_mode = 'points'
        if len(kwargs) > 0:
            self.set_data(**kwargs)
        self.freeze()
        return

    def set_data(self, pos=None, symbol='o', size=10.0, edge_width=1.0, edge_width_rel=None, edge_color='black', face_color='white', scaling=False):
        """ Set the data used to display this visual.

        Parameters
        ----------
        pos : array
            The array of locations to display each symbol.
        symbol : str
            The style of symbol to draw (see Notes).
        size : float or array
            The symbol size in px.
        edge_width : float | None
            The width of the symbol outline in pixels.
        edge_width_rel : float | None
            The width as a fraction of marker size. Exactly one of
            `edge_width` and `edge_width_rel` must be supplied.
        edge_color : Color | ColorArray
            The color used to draw each symbol outline.
        face_color : Color | ColorArray
            The color used to draw each symbol interior.
        scaling : bool
            If set to True, marker scales when rezooming.

        Notes
        -----
        Allowed style strings are: disc, arrow, ring, clobber, square, diamond,
        vbar, hbar, cross, tailed_arrow, x, triangle_up, triangle_down,
        and star.
        """
        assert isinstance(pos, np.ndarray) and pos.ndim == 2 and pos.shape[1] in (2,
                                                                                  3)
        if (edge_width is not None) + (edge_width_rel is not None) != 1:
            raise ValueError('exactly one of edge_width and edge_width_rel must be non-None')
        if edge_width is not None:
            if edge_width < 0:
                raise ValueError('edge_width cannot be negative')
        elif edge_width_rel < 0:
            raise ValueError('edge_width_rel cannot be negative')
        self.symbol = symbol
        self.scaling = scaling
        edge_color = ColorArray(edge_color).rgba
        if len(edge_color) == 1:
            edge_color = edge_color[0]
        face_color = ColorArray(face_color).rgba
        if len(face_color) == 1:
            face_color = face_color[0]
        n = len(pos)
        data = np.zeros(n, dtype=[('a_position', np.float32, 3),
         (
          'a_fg_color', np.float32, 4),
         (
          'a_bg_color', np.float32, 4),
         (
          'a_size', np.float32, 1),
         (
          'a_edgewidth', np.float32, 1)])
        data['a_fg_color'] = edge_color
        data['a_bg_color'] = face_color
        if edge_width is not None:
            data['a_edgewidth'] = edge_width
        else:
            data['a_edgewidth'] = size * edge_width_rel
        data['a_position'][:, :pos.shape[1]] = pos
        data['a_size'] = size
        self.shared_program['u_antialias'] = self.antialias
        self._data = data
        self._vbo.set_data(data)
        self.shared_program.bind(self._vbo)
        self.update()
        return

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        if symbol == self._symbol:
            return
        else:
            self._symbol = symbol
            if symbol is None:
                self._marker_fun = None
            else:
                _check_valid('symbol', symbol, marker_types)
                self._marker_fun = Function(_marker_dict[symbol])
                self._marker_fun['v_size'] = self._v_size_var
                self.shared_program.frag['marker'] = self._marker_fun
            self.update()
            return

    def _prepare_transforms(self, view):
        xform = view.transforms.get_transform()
        view.view_program.vert['transform'] = xform

    def _prepare_draw(self, view):
        if self._symbol is None:
            return False
        else:
            view.view_program['u_px_scale'] = view.transforms.pixel_scale
            if self.scaling:
                tr = view.transforms.get_transform('visual', 'document').simplified
                scale = np.linalg.norm((tr.map([1, 0]) - tr.map([0, 0]))[:2])
                view.view_program['u_scale'] = scale
            else:
                view.view_program['u_scale'] = 1
            return

    def _compute_bounds(self, axis, view):
        pos = self._data['a_position']
        if pos is None:
            return
        else:
            if pos.shape[1] > axis:
                return (pos[:, axis].min(), pos[:, axis].max())
            else:
                return (0, 0)

            return