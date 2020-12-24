# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\colors.py
# Compiled at: 2002-01-21 21:20:00
from types import StringType, IntType, InstanceType

class Color:
    """This class is used to represent color.  Components red, green, blue 
        are in the range 0 (dark) to 1 (full intensity)."""

    def __init__(self, red=0, green=0, blue=0):
        """Initialize with red, green, blue in range [0-1]."""
        _float = float
        d = self.__dict__
        d['red'] = _float(red)
        d['green'] = _float(green)
        d['blue'] = _float(blue)

    def __setattr__(self, name, value):
        raise TypeError, 'piddle.Color has read-only attributes'

    def __mul__(self, x):
        return Color(self.red * x, self.green * x, self.blue * x)

    def __rmul__(self, x):
        return Color(self.red * x, self.green * x, self.blue * x)

    def __div__(self, x):
        return Color(self.red / x, self.green / x, self.blue / x)

    def __rdiv__(self, x):
        return Color(self.red / x, self.green / x, self.blue / x)

    def __add__(self, x):
        return Color(self.red + x.red, self.green + x.green, self.blue + x.blue)

    def __sub__(self, x):
        return Color(self.red - x.red, self.green - x.green, self.blue - x.blue)

    def __repr__(self):
        return 'Color(%1.2f,%1.2f,%1.2f)' % (self.red, self.green, self.blue)

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __cmp__(self, other):
        try:
            dsum = 4 * self.red - 4 * other.red + 2 * self.green - 2 * other.green + self.blue - other.blue
        except:
            return -1

        if dsum > 0:
            return 1
        if dsum < 0:
            return -1
        return 0

    def toHexRGB(self):
        """Convert the color back to an integer suitable for the """
        r = int(255 * self.red)
        g = int(255 * self.green)
        b = int(255 * self.blue)
        return (r << 16) + (g << 8) + b

    def toHexStr(self):
        return '0x%.6x' % self.toHexRGB()


def HexColor(val):
    """This class converts a hex string, or an actual integer number,
        into the corresponding color.  E.g., in "AABBCC" or 0xAABBCC,
        AA is the red, BB is the green, and CC is the blue (00-FF)."""
    if type(val) == StringType:
        val = string.atoi(val, 16)
    factor = 1.0 / 255
    return Color(factor * (val >> 16 & 255), factor * (val >> 8 & 255), factor * (val & 255))


aliceblue = HexColor(15792383)
antiquewhite = HexColor(16444375)
aqua = HexColor(65535)
aquamarine = HexColor(8388564)
azure = HexColor(15794175)
beige = HexColor(16119260)
bisque = HexColor(16770244)
black = HexColor(0)
blanchedalmond = HexColor(16772045)
blue = HexColor(255)
blueviolet = HexColor(9055202)
brown = HexColor(10824234)
burlywood = HexColor(14596231)
cadetblue = HexColor(6266528)
chartreuse = HexColor(8388352)
chocolate = HexColor(13789470)
coral = HexColor(16744272)
cornflower = HexColor(6591981)
cornsilk = HexColor(16775388)
crimson = HexColor(14423100)
cyan = HexColor(65535)
darkblue = HexColor(139)
darkcyan = HexColor(35723)
darkgoldenrod = HexColor(12092939)
darkgray = HexColor(11119017)
darkgreen = HexColor(25600)
darkkhaki = HexColor(12433259)
darkmagenta = HexColor(9109643)
darkolivegreen = HexColor(5597999)
darkorange = HexColor(16747520)
darkorchid = HexColor(10040012)
darkred = HexColor(9109504)
darksalmon = HexColor(15308410)
darkseagreen = HexColor(9419915)
darkslateblue = HexColor(4734347)
darkslategray = HexColor(3100495)
darkturquoise = HexColor(52945)
darkviolet = HexColor(9699539)
deeppink = HexColor(16716947)
deepskyblue = HexColor(49151)
dimgray = HexColor(6908265)
dodgerblue = HexColor(2003199)
firebrick = HexColor(11674146)
floralwhite = HexColor(16775920)
forestgreen = HexColor(2263842)
fuchsia = HexColor(16711935)
gainsboro = HexColor(14474460)
ghostwhite = HexColor(16316671)
gold = HexColor(16766720)
goldenrod = HexColor(14329120)
gray = HexColor(8421504)
grey = gray
green = HexColor(32768)
greenyellow = HexColor(11403055)
honeydew = HexColor(15794160)
hotpink = HexColor(16738740)
indianred = HexColor(13458524)
indigo = HexColor(4915330)
ivory = HexColor(16777200)
khaki = HexColor(15787660)
lavender = HexColor(15132410)
lavenderblush = HexColor(16773365)
lawngreen = HexColor(8190976)
lemonchiffon = HexColor(16775885)
lightblue = HexColor(11393254)
lightcoral = HexColor(15761536)
lightcyan = HexColor(14745599)
lightgoldenrodyellow = HexColor(16448210)
lightgreen = HexColor(9498256)
lightgrey = HexColor(13882323)
lightpink = HexColor(16758465)
lightsalmon = HexColor(16752762)
lightseagreen = HexColor(2142890)
lightskyblue = HexColor(8900346)
lightslategray = HexColor(7833753)
lightsteelblue = HexColor(11584734)
lightyellow = HexColor(16777184)
lime = HexColor(65280)
limegreen = HexColor(3329330)
linen = HexColor(16445670)
magenta = HexColor(16711935)
maroon = HexColor(8388608)
mediumaquamarine = HexColor(6737322)
mediumblue = HexColor(205)
mediumorchid = HexColor(12211667)
mediumpurple = HexColor(9662683)
mediumseagreen = HexColor(3978097)
mediumslateblue = HexColor(8087790)
mediumspringgreen = HexColor(64154)
mediumturquoise = HexColor(4772300)
mediumvioletred = HexColor(13047173)
midnightblue = HexColor(1644912)
mintcream = HexColor(16121850)
mistyrose = HexColor(16770273)
moccasin = HexColor(16770229)
navajowhite = HexColor(16768685)
navy = HexColor(128)
oldlace = HexColor(16643558)
olive = HexColor(8421376)
olivedrab = HexColor(7048739)
orange = HexColor(16753920)
orangered = HexColor(16729344)
orchid = HexColor(14315734)
palegoldenrod = HexColor(15657130)
palegreen = HexColor(10025880)
paleturquoise = HexColor(11529966)
palevioletred = HexColor(14381203)
papayawhip = HexColor(16773077)
peachpuff = HexColor(16767673)
peru = HexColor(13468991)
pink = HexColor(16761035)
plum = HexColor(14524637)
powderblue = HexColor(11591910)
purple = HexColor(8388736)
red = HexColor(16711680)
rosybrown = HexColor(12357519)
royalblue = HexColor(4286945)
saddlebrown = HexColor(9127187)
salmon = HexColor(16416882)
sandybrown = HexColor(16032864)
seagreen = HexColor(3050327)
seashell = HexColor(16774638)
sienna = HexColor(10506797)
silver = HexColor(12632256)
skyblue = HexColor(8900331)
slateblue = HexColor(6970061)
slategray = HexColor(7372944)
snow = HexColor(16775930)
springgreen = HexColor(65407)
steelblue = HexColor(4620980)
tan = HexColor(13808780)
teal = HexColor(32896)
thistle = HexColor(14204888)
tomato = HexColor(16737095)
turquoise = HexColor(4251856)
violet = HexColor(15631086)
wheat = HexColor(16113331)
white = HexColor(16777215)
whitesmoke = HexColor(16119285)
yellow = HexColor(16776960)
yellowgreen = HexColor(10145074)
transparent = Color(-1, -1, -1)