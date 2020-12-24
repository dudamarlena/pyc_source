# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImagePalette.py
# Compiled at: 2007-09-25 20:00:35
import array, Image

class ImagePalette:
    """Colour palette for palette mapped images"""

    def __init__(self, mode='RGB', palette=None):
        self.mode = mode
        self.rawmode = None
        self.palette = palette or range(256) * len(self.mode)
        self.colors = {}
        self.dirty = None
        if len(self.mode) * 256 != len(self.palette):
            raise ValueError, 'wrong palette size'
        return

    def getdata(self):
        if self.rawmode:
            return (self.rawmode, self.palette)
        return (
         self.mode + ';L', self.tostring())

    def tostring(self):
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if Image.isStringType(self.palette):
            return self.palette
        return array.array('B', self.palette).tostring()

    def getcolor(self, color):
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if Image.isTupleType(color):
            try:
                return self.colors[color]
            except KeyError:
                if Image.isStringType(self.palette):
                    self.palette = map(int, self.palette)
                index = len(self.colors)
                if index >= 256:
                    raise ValueError('cannot allocate more than 256 colors')
                self.colors[color] = index
                self.palette[index] = color[0]
                self.palette[index + 256] = color[1]
                self.palette[index + 512] = color[2]
                self.dirty = 1
                return index

        else:
            raise ValueError('unknown color specifier: %r' % color)

    def save(self, fp):
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if type(fp) == type(''):
            fp = open(fp, 'w')
        fp.write('# Palette\n')
        fp.write('# Mode: %s\n' % self.mode)
        for i in range(256):
            fp.write('%d' % i)
            for j in range(i, len(self.palette), 256):
                fp.write(' %d' % self.palette[j])

            fp.write('\n')

        fp.close()


def raw(rawmode, data):
    palette = ImagePalette()
    palette.rawmode = rawmode
    palette.palette = data
    palette.dirty = 1
    return palette


def new(mode, data):
    return Image.core.new_palette(mode, data)


def negative(mode='RGB'):
    palette = range(256)
    palette.reverse()
    return ImagePalette(mode, palette * len(mode))


def random(mode='RGB'):
    from random import randint
    palette = map(lambda a, randint=randint: randint(0, 255), [0] * 256 * len(mode))
    return ImagePalette(mode, palette)


def wedge(mode='RGB'):
    return ImagePalette(mode, range(256) * len(mode))


def load(filename):
    fp = open(filename, 'rb')
    lut = None
    if not lut:
        try:
            import GimpPaletteFile
            fp.seek(0)
            p = GimpPaletteFile.GimpPaletteFile(fp)
            lut = p.getpalette()
        except (SyntaxError, ValueError):
            pass

    if not lut:
        try:
            import GimpGradientFile
            fp.seek(0)
            p = GimpGradientFile.GimpGradientFile(fp)
            lut = p.getpalette()
        except (SyntaxError, ValueError):
            pass

    if not lut:
        try:
            import PaletteFile
            fp.seek(0)
            p = PaletteFile.PaletteFile(fp)
            lut = p.getpalette()
        except (SyntaxError, ValueError):
            pass

    if not lut:
        raise IOError, 'cannot load palette'
    return lut