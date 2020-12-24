# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/context/color.py
# Compiled at: 2017-01-15 13:25:40
"""

A color context object

"""
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from ..compat import text_type, implements_to_string
from ..interface import AttributeExposer
from collections import OrderedDict
import colorsys, re
HTML_COLORS = {b'aqua': b'#00ffff', 
   b'aliceblue': b'#f0f8ff', 
   b'antiquewhite': b'#faebd7', 
   b'black': b'#000000', 
   b'blue': b'#0000ff', 
   b'cyan': b'#00ffff', 
   b'darkblue': b'#00008b', 
   b'darkcyan': b'#008b8b', 
   b'darkgreen': b'#006400', 
   b'darkturquoise': b'#00ced1', 
   b'deepskyblue': b'#00bfff', 
   b'green': b'#008000', 
   b'lime': b'#00ff00', 
   b'mediumblue': b'#0000cd', 
   b'mediumspringgreen': b'#00fa9a', 
   b'navy': b'#000080', 
   b'springgreen': b'#00ff7f', 
   b'teal': b'#008080', 
   b'midnightblue': b'#191970', 
   b'dodgerblue': b'#1e90ff', 
   b'lightseagreen': b'#20b2aa', 
   b'forestgreen': b'#228b22', 
   b'seagreen': b'#2e8b57', 
   b'darkslategray': b'#2f4f4f', 
   b'darkslategrey': b'#2f4f4f', 
   b'limegreen': b'#32cd32', 
   b'mediumseagreen': b'#3cb371', 
   b'turquoise': b'#40e0d0', 
   b'royalblue': b'#4169e1', 
   b'steelblue': b'#4682b4', 
   b'darkslateblue': b'#483d8b', 
   b'mediumturquoise': b'#48d1cc', 
   b'indigo': b'#4b0082', 
   b'darkolivegreen': b'#556b2f', 
   b'cadetblue': b'#5f9ea0', 
   b'cornflowerblue': b'#6495ed', 
   b'mediumaquamarine': b'#66cdaa', 
   b'dimgray': b'#696969', 
   b'dimgrey': b'#696969', 
   b'slateblue': b'#6a5acd', 
   b'olivedrab': b'#6b8e23', 
   b'slategray': b'#708090', 
   b'slategrey': b'#708090', 
   b'lightslategray': b'#778899', 
   b'lightslategrey': b'#778899', 
   b'mediumslateblue': b'#7b68ee', 
   b'lawngreen': b'#7cfc00', 
   b'aquamarine': b'#7fffd4', 
   b'chartreuse': b'#7fff00', 
   b'gray': b'#808080', 
   b'grey': b'#808080', 
   b'maroon': b'#800000', 
   b'olive': b'#808000', 
   b'purple': b'#800080', 
   b'lightskyblue': b'#87cefa', 
   b'skyblue': b'#87ceeb', 
   b'blueviolet': b'#8a2be2', 
   b'darkmagenta': b'#8b008b', 
   b'darkred': b'#8b0000', 
   b'saddlebrown': b'#8b4513', 
   b'darkseagreen': b'#8fbc8f', 
   b'lightgreen': b'#90ee90', 
   b'mediumpurple': b'#9370db', 
   b'darkviolet': b'#9400d3', 
   b'palegreen': b'#98fb98', 
   b'darkorchid': b'#9932cc', 
   b'yellowgreen': b'#9acd32', 
   b'sienna': b'#a0522d', 
   b'brown': b'#a52a2a', 
   b'darkgray': b'#a9a9a9', 
   b'darkgrey': b'#a9a9a9', 
   b'greenyellow': b'#adff2f', 
   b'lightblue': b'#add8e6', 
   b'paleturquoise': b'#afeeee', 
   b'lightsteelblue': b'#b0c4de', 
   b'powderblue': b'#b0e0e6', 
   b'firebrick': b'#b22222', 
   b'darkgoldenrod': b'#b8860b', 
   b'mediumorchid': b'#ba55d3', 
   b'rosybrown': b'#bc8f8f', 
   b'darkkhaki': b'#bdb76b', 
   b'silver': b'#c0c0c0', 
   b'mediumvioletred': b'#c71585', 
   b'indianred': b'#cd5c5c', 
   b'peru': b'#cd853f', 
   b'chocolate': b'#d2691e', 
   b'tan': b'#d2b48c', 
   b'lightgray': b'#d3d3d3', 
   b'lightgrey': b'#d3d3d3', 
   b'thistle': b'#d8bfd8', 
   b'goldenrod': b'#daa520', 
   b'orchid': b'#da70d6', 
   b'palevioletred': b'#db7093', 
   b'crimson': b'#dc143c', 
   b'gainsboro': b'#dcdcdc', 
   b'plum': b'#dda0dd', 
   b'burlywood': b'#deb887', 
   b'lightcyan': b'#e0ffff', 
   b'lavender': b'#e6e6fa', 
   b'darksalmon': b'#e9967a', 
   b'palegoldenrod': b'#eee8aa', 
   b'violet': b'#ee82ee', 
   b'azure': b'#f0ffff', 
   b'honeydew': b'#f0fff0', 
   b'khaki': b'#f0e68c', 
   b'lightcoral': b'#f08080', 
   b'sandybrown': b'#f4a460', 
   b'beige': b'#f5f5dc', 
   b'mintcream': b'#f5fffa', 
   b'wheat': b'#f5deb3', 
   b'whitesmoke': b'#f5f5f5', 
   b'ghostwhite': b'#f8f8ff', 
   b'lightgoldenrodyellow': b'#fafad2', 
   b'linen': b'#faf0e6', 
   b'salmon': b'#fa8072', 
   b'oldlace': b'#fdf5e6', 
   b'bisque': b'#ffe4c4', 
   b'blanchedalmond': b'#ffebcd', 
   b'coral': b'#ff7f50', 
   b'cornsilk': b'#fff8dc', 
   b'darkorange': b'#ff8c00', 
   b'deeppink': b'#ff1493', 
   b'floralwhite': b'#fffaf0', 
   b'fuchsia': b'#ff00ff', 
   b'gold': b'#ffd700', 
   b'hotpink': b'#ff69b4', 
   b'ivory': b'#fffff0', 
   b'lavenderblush': b'#fff0f5', 
   b'lemonchiffon': b'#fffacd', 
   b'lightpink': b'#ffb6c1', 
   b'lightsalmon': b'#ffa07a', 
   b'lightyellow': b'#ffffe0', 
   b'magenta': b'#ff00ff', 
   b'mistyrose': b'#ffe4e1', 
   b'moccasin': b'#ffe4b5', 
   b'navajowhite': b'#ffdead', 
   b'orange': b'#ffa500', 
   b'orangered': b'#ff4500', 
   b'papayawhip': b'#ffefd5', 
   b'peachpuff': b'#ffdab9', 
   b'pink': b'#ffc0cb', 
   b'red': b'#ff0000', 
   b'seashell': b'#fff5ee', 
   b'snow': b'#fffafa', 
   b'tomato': b'#ff6347', 
   b'white': b'#ffffff', 
   b'yellow': b'#ffff00', 
   b'rebeccapurple': b'#663399'}
HTML_COLORS[b'transparent'] = b'rgba(0,0,0,0)'

@implements_to_string
class Color(AttributeExposer):
    """HTML color object"""
    __moya_exposed_attributes__ = [
     b'r', b'g', b'b', b'a',
     b'rgb', b'rgba', b'hsl', b'hsla',
     b'html', b'hex',
     b'name',
     b'opaque', b'saturated']
    _re_hex = re.compile(b'^\\#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})$')
    _re_hex_short = re.compile(b'^\\#([a-fA-F0-9]{1})([a-fA-F0-9]{1})([a-fA-F0-9]{1})$')
    _re_rgb = re.compile(b'rgb\\(\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\s*\\)')
    _re_rgba = re.compile(b'rgba\\(\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\s*\\)')
    _re_hsl = re.compile(b'hsl\\(\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\%\\s*,\\s*([0-9\\.]+)\\%\\s*\\)')
    _re_hsla = re.compile(b'hsla\\(\\s*([0-9\\.]+)\\s*,\\s*([0-9\\.]+)\\%\\s*,\\s*([0-9\\.]+)\\%\\s*,\\s*([0-9\\.]+)\\s*\\)')

    def __init__(self, r, g, b, a=1.0):
        self._r = float(r)
        self._g = float(g)
        self._b = float(b)
        self._a = float(a)

    def copy(self):
        return Color(self._r, self._g, self._b, self._a)

    @classmethod
    def construct(cls, context, obj):
        if isinstance(obj, cls):
            return obj.copy()
        if isinstance(obj, text_type):
            return cls.parse(obj)
        if isinstance(obj, (float, int)):
            return cls(obj, obj, obj)
        try:
            r, g, b, a = obj
        except:
            pass
        else:
            return cls(r, g, b, a)

        try:
            r, g, b = obj
        except:
            pass
        else:
            return cls(r, g, b)

        raise ValueError((b'unable to convert {} to a color').format(context.to_expr(obj)))

    @classmethod
    def parse(cls, txt):
        txt = txt.strip().lower()
        if txt == b'inherit':
            return b'inherit'
        if txt in HTML_COLORS:
            return HTML_COLORS[txt]
        if txt.startswith(b'#'):
            return cls.parse_hex(txt)
        if txt.startswith(b'rgba'):
            return cls.parse_rgba(txt)
        if txt.startswith(b'rgb'):
            return cls.parse_rgb(txt)
        if txt.startswith(b'hsla'):
            return cls.parse_hsla(txt)
        if txt.startswith(b'hsl'):
            return cls.parse_hsl(txt)
        raise ValueError((b"unable to parse '{}' as a color").format(txt))

    @classmethod
    def parse_hex(cls, hex):
        match = cls._re_hex_short.match(hex)
        if match is not None:
            r, g, b = [ int(c + c, 16) for c in match.groups() ]
            return cls(r, g, b)
        else:
            match = cls._re_hex.match(hex)
            if match is None:
                raise ValueError(b'not valid hex color')
            r, g, b = [ int(c, 16) for c in match.groups() ]
            return cls(r, g, b)
            return

    @classmethod
    def parse_rgb(cls, rgb):
        match = cls._re_rgb.match(rgb)
        if match is None:
            raise ValueError(b'not a valid rgb color')
        r, g, b = [ int(c) for c in match.groups() ]
        return cls(r, g, b)

    @classmethod
    def parse_rgba(cls, rgba):
        match = cls._re_rgba.match(rgba)
        if match is None:
            raise ValueError(b'not a valid rgb color')
        r, g, b = [ int(c) for c in match.groups()[:3] ]
        a = float(match.groups()[3])
        return cls(r, g, b, a)

    @classmethod
    def parse_hsl(cls, hsl):
        match = cls._re_hsl.match(hsl)
        if match is None:
            raise ValueError(b'not a valid hsl color')
        h, s, l = [ float(c) for c in match.groups() ]
        h = h / 360.0
        l = l / 100.0
        s = s / 100.0
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return cls(r * 255.0, g * 255.0, b * 255.0)

    @classmethod
    def parse_hsla(cls, hsla):
        match = cls._re_hsla.match(hsla)
        if match is None:
            raise ValueError(b'not a valid hsla color')
        h, s, l, a = [ float(c) for c in match.groups() ]
        h = h / 360.0
        l = l / 100.0
        s = s / 100.0
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return cls(r * 255.0, g * 255.0, b * 255.0, a * 255.0)

    def __moyaconsole__(self, console):
        from moya import pilot
        link = (b'http://www.color-hex.com/color/{}').format(self.hex.lower()[1:])
        mr = self.__moyarepr__(pilot.context)
        console.text(mr, bold=True)
        console.text(link, fg=b'cyan', underline=True)

    def __str__(self):
        return self.html

    def __repr__(self):
        return (b'Color({!r}, {!r}, {!r}, {!r})').format(self._r, self._g, self._b, self._a)

    def __moyarepr__(self, context):
        return (b'color:[{:g}, {:g}, {:g}, {:g}]').format(self._r, self._g, self._b, self._a)

    def __hash__(self):
        return hash((self._r, self._g, self._b, self._a))

    def as_pillow_tuple(self):
        if self.a == 1.0:
            return (int(self.r), int(self.g), int(self.b))
        else:
            return (
             int(self.r), int(self.g), int(self.b), int(self.a * 255.0))

    @property
    def html(self):
        if self.a == 1.0:
            return self.hex
        else:
            return self.rgba

    @property
    def hex(self):
        if any(c % 17 for c in self._rgb):
            return (b'#{:02X}{:02X}{:02X}').format(*self._rgb)
        else:
            return (b'#{:0X}{:0X}{:0X}').format(*(c // 17 for c in self._rgb))

    @property
    def rgb(self):
        return (b'rgb({},{},{})').format(*self._rgb)

    @property
    def rgba(self):
        return (b'rgba({},{},{},{:g})').format(*self._rgba)

    @property
    def hsl(self):
        h, l, s = colorsys.rgb_to_hls(self.r / 255.0, self.g / 255.0, self.b / 255.0)
        return (b'hsl({:g},{:g}%,{:g}%)').format(h * 360.0, s * 100.0, l * 100.0)

    @property
    def hsla(self):
        h, l, s = colorsys.rgb_to_hls(self.r / 255.0, self.g / 255.0, self.b / 255.0)
        return (b'hsla({:g},{:g}%,{:g}%,{:g})').format(h * 360.0, s * 100.0, l * 100.0, self.a)

    @property
    def _rgb(self):
        return [int(self.r), int(self.g), int(self.b)]

    @property
    def _rgba(self):
        return [int(self.r), int(self.g), int(self.b), int(self.a)]

    @property
    def _rgb_raw(self):
        return (self._r, self._g, self._b)

    @property
    def _rgba_raw(self):
        return (self._r, self._g, self._b, self._a)

    @property
    def opaque(self):
        return Color(self._r, self._g, self._b, 1.0)

    @property
    def saturated(self):
        return Color(self.r, self.g, self.b, self.a)

    @property
    def r(self):
        return min(255.0, max(0.0, self._r))

    @property
    def g(self):
        return min(255.0, max(0.0, self._g))

    @property
    def b(self):
        return min(255.0, max(0.0, self._b))

    @property
    def a(self):
        return min(1.0, max(0.0, self._a))

    @property
    def name(self):
        return HTML_COLORS_REVERSE.get(self, None)

    def __eq__(self, other):
        if not isinstance(other, Color):
            raise ValueError(b'can only compare a color to another color')
        return self._r == other._r and self._g == other._g and self._b == other._b and self._a == other._a

    def __add__(self, other):
        if not isinstance(other, Color):
            raise ValueError(b'can only add another color to a color')
        r, g, b, a = self._rgba_raw
        _r, _g, _b, _a = other._rgba_raw
        return Color(r + _r, g + _g, b + _b, a)

    def __sub__(self, other):
        if not isinstance(other, Color):
            raise ValueError(b'can only subtract another color from a color')
        r, g, b, a = self._rgba_raw
        _r, _g, _b, _a = other._rgba_raw
        return Color(r - _r, g - _g, b - _b, a)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            other = float(other)
            r, g, b, a = self._rgba_raw
            return Color(r * other, g * other, b * other, a)
        if not isinstance(other, Color):
            raise ValueError(b'can only multiple a color by a number or other color')
        r, g, b, a = self._rgba_raw
        _r, _g, _b, _a = other._rgba_raw
        return Color(r * _r, g * _g, b * _b, a)

    def __div__(self, other):
        raise NotImplementedError(b"can't divide a color")


HTML_COLORS = {k:Color.parse(v) for k, v in HTML_COLORS.items()}
HTML_COLORS_REVERSE = {v:k for k, v in HTML_COLORS.items()}
if __name__ == b'__main__':
    print(unicode(Color(20, 255, 0)))
    print(unicode(Color(20, 255, 0, 0.5)))
    print(unicode(Color.parse_hex(b'#00FF34').html))
    print(unicode(Color.parse_rgb(b'rgb(100, 23,50)').html))
    print(unicode(Color.parse_rgba(b'rgba(100, 23,50, 0.6)').html))
    print(Color.parse(b'tomato'))
    print(Color.parse(b'white'))
    print(Color.parse(b'hsl(200, 50%, 10%)'))
    print(Color.parse(b'hsla(200, 50%, 10%, 0.5)'))
    print(Color.parse(b'hsl(120, 100%, 50%)'))