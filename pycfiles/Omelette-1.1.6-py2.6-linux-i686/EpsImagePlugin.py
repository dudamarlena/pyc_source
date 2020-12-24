# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/EpsImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.5'
import re, string, Image, ImageFile

def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


def o32(i):
    return chr(i & 255) + chr(i >> 8 & 255) + chr(i >> 16 & 255) + chr(i >> 24 & 255)


split = re.compile('^%%([^:]*):[ \\t]*(.*)[ \\t]*$')
field = re.compile('^%[%!\\w]([^:]*)[ \\t]*$')

def Ghostscript(tile, size, fp):
    """Render an image using Ghostscript (Unix only)"""
    (decoder, tile, offset, data) = tile[0]
    (length, bbox) = data
    import tempfile, os
    file = tempfile.mktemp()
    command = [
     'gs',
     '-q',
     '-g%dx%d' % size,
     '-dNOPAUSE -dSAFER',
     '-sDEVICE=ppmraw',
     '-sOutputFile=%s' % file,
     '- >/dev/null 2>/dev/null']
    command = string.join(command)
    try:
        gs = os.popen(command, 'w')
        if bbox[0] != 0 or bbox[1] != 0:
            gs.write('%d %d translate\n' % (-bbox[0], -bbox[1]))
        fp.seek(offset)
        while length > 0:
            s = fp.read(8192)
            if not s:
                break
            length = length - len(s)
            gs.write(s)

        status = gs.close()
        if status:
            raise IOError('gs failed (status %d)' % status)
        im = Image.core.open_ppm(file)
    finally:
        try:
            os.unlink(file)
        except:
            pass

    return im


class PSFile:
    """Wrapper that treats either CR or LF as end of line."""

    def __init__(self, fp):
        self.fp = fp
        self.char = None
        return

    def __getattr__(self, id):
        v = getattr(self.fp, id)
        setattr(self, id, v)
        return v

    def seek(self, offset, whence=0):
        self.char = None
        self.fp.seek(offset, whence)
        return

    def tell(self):
        pos = self.fp.tell()
        if self.char:
            pos = pos - 1
        return pos

    def readline(self):
        s = ''
        if self.char:
            c = self.char
            self.char = None
        else:
            c = self.fp.read(1)
        while c not in '\r\n':
            s = s + c
            c = self.fp.read(1)

        if c == '\r':
            self.char = self.fp.read(1)
            if self.char == '\n':
                self.char = None
        return s + '\n'


def _accept(prefix):
    return prefix[:4] == '%!PS' or i32(prefix) == 3335770309


class EpsImageFile(ImageFile.ImageFile):
    """EPS File Parser for the Python Imaging Library"""
    format = 'EPS'
    format_description = 'Encapsulated Postscript'

    def _open(self):
        fp = PSFile(self.fp)
        s = fp.read(512)
        if s[:4] == '%!PS':
            offset = 0
            fp.seek(0, 2)
            length = fp.tell()
        elif i32(s) == 3335770309:
            offset = i32(s[4:])
            length = i32(s[8:])
            fp.seek(offset)
        else:
            raise SyntaxError, 'not an EPS file'
        fp.seek(offset)
        box = None
        self.mode = 'RGB'
        self.size = (1, 1)
        s = fp.readline()
        while s:
            if len(s) > 255:
                raise SyntaxError, 'not an EPS file'
            if s[-2:] == '\r\n':
                s = s[:-2]
            elif s[-1:] == '\n':
                s = s[:-1]
            try:
                m = split.match(s)
            except re.error, v:
                raise SyntaxError, 'not an EPS file'

            if m:
                (k, v) = m.group(1, 2)
                self.info[k] = v
                if k == 'BoundingBox':
                    try:
                        box = map(int, map(float, string.split(v)))
                        self.size = (box[2] - box[0], box[3] - box[1])
                        self.tile = [
                         ('eps', (0, 0) + self.size, offset,
                          (
                           length, box))]
                    except:
                        pass

            else:
                m = field.match(s)
                if m:
                    k = m.group(1)
                    if k == 'EndComments':
                        break
                    if k[:8] == 'PS-Adobe':
                        self.info[k[:8]] = k[9:]
                    else:
                        self.info[k] = ''
                else:
                    raise IOError, 'bad EPS header'
            s = fp.readline()
            if s[:1] != '%':
                break

        while s[0] == '%':
            if len(s) > 255:
                raise SyntaxError, 'not an EPS file'
            if s[-2:] == '\r\n':
                s = s[:-2]
            elif s[-1:] == '\n':
                s = s[:-1]
            if s[:11] == '%ImageData:':
                (x, y, bi, mo, z3, z4, en, id) = string.split(s[11:], maxsplit=7)
                x = int(x)
                y = int(y)
                bi = int(bi)
                mo = int(mo)
                en = int(en)
                if en == 1:
                    decoder = 'eps_binary'
                elif en == 2:
                    decoder = 'eps_hex'
                else:
                    break
                if bi != 8:
                    break
                if mo == 1:
                    self.mode = 'L'
                elif mo == 2:
                    self.mode = 'LAB'
                elif mo == 3:
                    self.mode = 'RGB'
                else:
                    break
                if id[:1] == id[-1:] == '"':
                    id = id[1:-1]
                while 1:
                    s = fp.readline()
                    if not s:
                        break
                    if s[:len(id)] == id:
                        self.size = (
                         x, y)
                        self.tile2 = [
                         (decoder,
                          (
                           0, 0, x, y),
                          fp.tell(),
                          0)]
                        return

            s = fp.readline()
            if not s:
                break

        if not box:
            raise IOError, 'cannot determine EPS bounding box'
        return

    def load(self):
        if not self.tile:
            return
        self.im = Ghostscript(self.tile, self.size, self.fp)
        self.mode = self.im.mode
        self.size = self.im.size
        self.tile = []


def _save(im, fp, filename, eps=1):
    """EPS Writer for the Python Imaging Library."""
    im.load()
    if im.mode == 'L':
        operator = (8, 1, 'image')
    elif im.mode == 'RGB':
        operator = (8, 3, 'false 3 colorimage')
    elif im.mode == 'CMYK':
        operator = (8, 4, 'false 4 colorimage')
    else:
        raise ValueError, 'image mode is not supported'
    if eps:
        fp.write('%!PS-Adobe-3.0 EPSF-3.0\n')
        fp.write('%%Creator: PIL 0.1 EpsEncode\n')
        fp.write('%%%%BoundingBox: 0 0 %d %d\n' % im.size)
        fp.write('%%Pages: 1\n')
        fp.write('%%EndComments\n')
        fp.write('%%Page: 1 1\n')
        fp.write('%%ImageData: %d %d ' % im.size)
        fp.write('%d %d 0 1 1 "%s"\n' % operator)
    fp.write('gsave\n')
    fp.write('10 dict begin\n')
    fp.write('/buf %d string def\n' % (im.size[0] * operator[1]))
    fp.write('%d %d scale\n' % im.size)
    fp.write('%d %d 8\n' % im.size)
    fp.write('[%d 0 0 -%d 0 %d]\n' % (im.size[0], im.size[1], im.size[1]))
    fp.write('{ currentfile buf readhexstring pop } bind\n')
    fp.write('%s\n' % operator[2])
    ImageFile._save(im, fp, [('eps', (0, 0) + im.size, 0, None)])
    fp.write('\n%%%%EndBinary\n')
    fp.write('grestore end\n')
    fp.flush()
    return


Image.register_open(EpsImageFile.format, EpsImageFile, _accept)
Image.register_save(EpsImageFile.format, _save)
Image.register_extension(EpsImageFile.format, '.ps')
Image.register_extension(EpsImageFile.format, '.eps')
Image.register_mime(EpsImageFile.format, 'application/postscript')