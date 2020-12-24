# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/IptcImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.3'
import Image, ImageFile, os, tempfile
COMPRESSION = {1: 'raw', 
   5: 'jpeg'}
PAD = chr(0) * 4

def i16(c):
    return ord(c[1]) + (ord(c[0]) << 8)


def i32(c):
    return ord(c[3]) + (ord(c[2]) << 8) + (ord(c[1]) << 16) + (ord(c[0]) << 24)


def i(c):
    return i32((PAD + c)[-4:])


def dump(c):
    for i in c:
        print '%02x' % ord(i),

    print


class IptcImageFile(ImageFile.ImageFile):
    format = 'IPTC'
    format_description = 'IPTC/NAA'

    def getint(self, key):
        return i(self.info[key])

    def field(self):
        s = self.fp.read(5)
        if not len(s):
            return (None, 0)
        else:
            tag = (
             ord(s[1]), ord(s[2]))
            if ord(s[0]) != 28 or tag[0] < 1 or tag[0] > 9:
                raise SyntaxError, 'invalid IPTC/NAA file'
            size = ord(s[3])
            if size > 132:
                raise IOError, 'illegal field length in IPTC/NAA file'
            elif size == 128:
                size = 0
            elif size > 128:
                size = i(self.fp.read(size - 128))
            else:
                size = i16(s[3:])
            return (tag, size)

    def _is_raw(self, offset, size):
        return 0
        self.fp.seek(offset)
        (t, sz) = self.field()
        if sz != size[0]:
            return 0
        y = 1
        while 1:
            self.fp.seek(sz, 1)
            (t, s) = self.field()
            if t != (8, 10):
                break
            if s != sz:
                return 0
            y = y + 1

        return y == size[1]

    def _open(self):
        while 1:
            offset = self.fp.tell()
            (tag, size) = self.field()
            if not tag or tag == (8, 10):
                break
            if size:
                self.info[tag] = self.fp.read(size)
            else:
                self.info[tag] = None

        layers = ord(self.info[(3, 60)][0])
        component = ord(self.info[(3, 60)][1])
        if self.info.has_key((3, 65)):
            id = ord(self.info[(3, 65)][0]) - 1
        else:
            id = 0
        if layers == 1 and not component:
            self.mode = 'L'
        elif layers == 3 and component:
            self.mode = 'RGB'[id]
        elif layers == 4 and component:
            self.mode = 'CMYK'[id]
        self.size = (
         self.getint((3, 20)), self.getint((3, 30)))
        try:
            compression = COMPRESSION[self.getint((3, 120))]
        except KeyError:
            raise IOError, 'Unknown IPTC image compression'

        if tag == (8, 10):
            if compression == 'raw' and self._is_raw(offset, self.size):
                self.tile = [(
                  compression, (offset, size + 5, -1),
                  (
                   0, 0, self.size[0], self.size[1]))]
            else:
                self.tile = [
                 (
                  'iptc', (compression, offset),
                  (
                   0, 0, self.size[0], self.size[1]))]
        return

    def load(self):
        if len(self.tile) != 1 or self.tile[0][0] != 'iptc':
            return ImageFile.ImageFile.load(self)
        (type, tile, box) = self.tile[0]
        (encoding, offset) = tile
        self.fp.seek(offset)
        outfile = tempfile.mktemp()
        o = open(outfile, 'wb')
        if encoding == 'raw':
            o.write('P5\n%d %d\n255\n' % self.size)
        while 1:
            (type, size) = self.field()
            if type != (8, 10):
                break
            while size > 0:
                s = self.fp.read(min(size, 8192))
                if not s:
                    break
                o.write(s)
                size = size - len(s)

        o.close()
        try:
            try:
                self.im = Image.core.open_ppm(outfile)
            except:
                im = Image.open(outfile)
                im.load()
                self.im = im.im

        finally:
            try:
                os.unlink(outfile)
            except:
                pass


Image.register_open('IPTC', IptcImageFile)
Image.register_extension('IPTC', '.iim')

def getiptcinfo(im):
    import TiffImagePlugin, JpegImagePlugin, StringIO
    data = None
    if isinstance(im, IptcImageFile):
        return im.info
    else:
        if isinstance(im, JpegImagePlugin.JpegImageFile):
            try:
                app = im.app['APP13']
                if app[:14] == 'Photoshop 3.0\x00':
                    app = app[14:]
                    offset = 0
                    while app[offset:offset + 4] == '8BIM':
                        offset = offset + 4
                        code = JpegImagePlugin.i16(app, offset)
                        offset = offset + 2
                        name_len = ord(app[offset])
                        name = app[offset + 1:offset + 1 + name_len]
                        offset = 1 + offset + name_len
                        if offset & 1:
                            offset = offset + 1
                        size = JpegImagePlugin.i32(app, offset)
                        offset = offset + 4
                        if code == 1028:
                            data = app[offset:offset + size]
                            break
                        offset = offset + size
                        if offset & 1:
                            offset = offset + 1

            except (AttributeError, KeyError):
                pass

        elif isinstance(im, TiffImagePlugin.TiffImageFile):
            try:
                (type, data) = im.tag.tagdata[TiffImagePlugin.IPTC_NAA_CHUNK]
            except (AttributeError, KeyError):
                pass

        if data is None:
            return

        class FakeImage:
            pass

        im = FakeImage()
        im.__class__ = IptcImageFile
        im.info = {}
        im.fp = StringIO.StringIO(data)
        try:
            im._open()
        except (IndexError, KeyError):
            pass

        return im.info