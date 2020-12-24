# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/filters/color.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 5435 bytes
import weakref
from ..shaders import Function, Varying
from ...color import colormap, Color

class IsolineFilter(object):

    def __init__(self, level=2.0, width=2.0, antialias=1.0, color='black'):
        self.fshader = Function('\n            void isoline() {\n                if ($isolevel <= 0 || $isowidth <= 0) {\n                    return;\n                }\n\n                // function taken from glumpy/examples/isocurves.py\n                // and extended to have level, width, color and antialiasing\n                // as parameters\n\n                // Extract data value\n                // this accounts for perception,\n                // have to decide, which one to use or make this a uniform\n                const vec3 w = vec3(0.299, 0.587, 0.114);\n                //const vec3 w = vec3(0.2126, 0.7152, 0.0722);\n                float value = dot(gl_FragColor.rgb, w);\n\n                // setup lw, aa\n                float linewidth = $isowidth + $antialias;\n\n                // "middle" contour(s) dividing upper and lower half\n                // but only if isolevel is even\n                if( mod($isolevel,2.0) == 0.0 ) {\n                    if( length(value - 0.5) < 0.5 / $isolevel)\n                        linewidth = linewidth * 2;\n                }\n\n                // Trace contour isoline\n                float v  = $isolevel * value - 0.5;\n                float dv = linewidth/2.0 * fwidth(v);\n                float f = abs(fract(v) - 0.5);\n                float d = smoothstep(-dv, +dv, f);\n                float t = linewidth/2.0 - $antialias;\n                d = abs(d)*linewidth/2.0 - t;\n\n                if( d < - linewidth ) {\n                    d = 1.0;\n                } else  {\n                     d /= $antialias;\n                }\n\n                // setup foreground\n                vec4 fc = $isocolor;\n\n                // mix with background\n                if (d < 1.) {\n                    gl_FragColor = mix(gl_FragColor, fc, 1-d);\n                }\n\n            }\n        ')
        self.level = level
        self.width = width
        self.color = color
        self.antialias = antialias
        self.isoline_expr = self.fshader()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, l):
        if l <= 0:
            l = 0
        self._level = l
        self.fshader['isolevel'] = l

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w
        self.fshader['isowidth'] = w

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c
        self.fshader['isocolor'] = Color(c).rgba

    @property
    def antialias(self):
        return self._antialias

    @antialias.setter
    def antialias(self, a):
        self._antialias = a
        self.fshader['antialias'] = a

    def _attach(self, visual):
        hook = visual._get_hook('frag', 'post')
        hook.add(self.isoline_expr)


class Alpha(object):

    def __init__(self, alpha=1.0):
        self.shader = Function('\n            void apply_alpha() {\n                gl_FragColor.a = gl_FragColor.a * $alpha;\n            }\n        ')
        self.alpha = alpha

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, a):
        self._alpha = a
        self.shader['alpha'] = a

    def _attach(self, visual):
        self._visual = weakref.ref(visual)
        hook = visual._get_hook('frag', 'post')
        hook.add(self.shader())


class ColorFilter(object):

    def __init__(self, filter=(1, 1, 1, 1)):
        self.shader = Function('\n            void apply_color_filter() {\n                gl_FragColor = gl_FragColor * $filter;\n            }\n        ')
        self.filter = filter

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, f):
        self._filter = tuple(f)
        self.shader['filter'] = self._filter

    def _attach(self, visual):
        self._visual = visual
        hook = visual._get_hook('frag', 'post')
        hook.add((self.shader()), position=8)


class ZColormapFilter(object):

    def __init__(self, cmap, zrange=(0, 1)):
        self.vshader = Function('\n            void z_colormap_support() {\n                $zval = $position.z;\n            }\n        ')
        self.fshader = Function('\n            void apply_z_colormap() {\n                gl_FragColor = $cmap(($zval - $zrange.x) /\n                                        ($zrange.y - $zrange.x));\n            }\n        ')
        if isinstance(cmap, str):
            cmap = colormap.get_colormap(cmap)
        self.cmap = Function(cmap.glsl_map)
        self.fshader['cmap'] = self.cmap
        self.fshader['zrange'] = zrange
        self.vshader['zval'] = Varying('v_zval', dtype='float')
        self.fshader['zval'] = self.vshader['zval']

    def _attach(self, visual):
        self._visual = visual
        vhook = visual._get_hook('vert', 'post')
        vhook.add((self.vshader()), position=9)
        fhook = visual._get_hook('frag', 'post')
        fhook.add((self.fshader()), position=3)
        self.vshader['position'] = visual.shared_program.vert['position']