# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImageFile.py
# Compiled at: 2007-09-25 20:00:35
import Image, traceback, sys, string, os
MAXBLOCK = 65536
SAFEBLOCK = 1048576
ERRORS = {-1: 'image buffer overrun error', 
   -2: 'decoding error', 
   -3: 'unknown error', 
   -8: 'bad configuration', 
   -9: 'out of memory error'}

def _tilesort(t1, t2):
    return cmp(t1[2], t2[2])


class ImageFile(Image.Image):
    """Base class for image file format handlers."""

    def __init__(self, fp=None, filename=None):
        Image.Image.__init__(self)
        self.tile = None
        self.readonly = 1
        self.decoderconfig = ()
        self.decodermaxblock = MAXBLOCK
        if Image.isStringType(fp):
            self.fp = open(fp, 'rb')
            self.filename = fp
        else:
            self.fp = fp
            self.filename = filename
        try:
            self._open()
        except IndexError, v:
            if Image.DEBUG > 1:
                traceback.print_exc()
            raise SyntaxError, v
        except TypeError, v:
            if Image.DEBUG > 1:
                traceback.print_exc()
            raise SyntaxError, v
        except KeyError, v:
            if Image.DEBUG > 1:
                traceback.print_exc()
            raise SyntaxError, v
        except EOFError, v:
            if Image.DEBUG > 1:
                traceback.print_exc()
            raise SyntaxError, v

        if not self.mode or self.size[0] <= 0:
            raise SyntaxError, 'not identified by this driver'
        return

    def draft(self, mode, size):
        """Set draft mode"""
        pass

    def verify(self):
        """Check file integrity"""
        self.fp = None
        return

    def load(self):
        """Load image data based on tile list"""
        pixel = Image.Image.load(self)
        if self.tile is None:
            raise IOError('cannot load this image')
        if not self.tile:
            return pixel
        else:
            self.map = None
            readonly = 0
            if self.filename:
                if len(self.tile) == 1:
                    (d, e, o, a) = self.tile[0]
                    if d == 'raw' and a[0] == self.mode and a[0] in Image._MAPMODES:
                        try:
                            if hasattr(Image.core, 'map'):
                                self.map = Image.core.map(self.filename)
                                self.map.seek(o)
                                self.im = self.map.readimage(self.mode, self.size, a[1], a[2])
                            else:
                                import mmap
                                file = open(self.filename, 'r+')
                                size = os.path.getsize(self.filename)
                                self.map = mmap.mmap(file.fileno(), size)
                                self.im = Image.core.map_buffer(self.map, self.size, d, e, o, a)
                            readonly = 1
                        except (AttributeError, EnvironmentError, ImportError):
                            self.map = None

                self.load_prepare()
                try:
                    read = self.load_read
                except AttributeError:
                    read = self.fp.read
                else:
                    try:
                        seek = self.load_seek
                    except AttributeError:
                        seek = self.fp.seek
                    else:
                        self.map or self.tile.sort(_tilesort)
                        try:
                            prefix = self.tile_prefix
                        except AttributeError:
                            prefix = ''
                        else:
                            for (d, e, o, a) in self.tile:
                                d = Image._getdecoder(self.mode, d, a, self.decoderconfig)
                                seek(o)
                                try:
                                    d.setimage(self.im, e)
                                except ValueError:
                                    continue

                                b = prefix
                                t = len(b)
                                while 1:
                                    s = read(self.decodermaxblock)
                                    if not s:
                                        self.tile = []
                                        raise IOError('image file is truncated (%d bytes not processed)' % len(b))
                                    b = b + s
                                    (n, e) = d.decode(b)
                                    if n < 0:
                                        break
                                    b = b[n:]
                                    t = t + n

            self.tile = []
            self.readonly = readonly
            self.fp = None
            if not self.map and e < 0:
                error = ERRORS.get(e, 'decoder error %d' % e)
                raise IOError(error + ' when reading image file')
            if hasattr(self, 'tile_post_rotate'):
                self.im = self.im.rotate(self.tile_post_rotate)
                self.size = self.im.size
            self.load_end()
            return Image.Image.load(self)

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.new(self.mode, self.size)
        if self.mode == 'P':
            Image.Image.load(self)

    def load_end(self):
        pass


class StubImageFile(ImageFile):
    """Base class for stub image loaders."""

    def _open(self):
        raise NotImplementedError('StubImageFile subclass must implement _open')

    def load(self):
        loader = self._load()
        if loader is None:
            raise IOError('cannot find loader for this %s file' % self.format)
        image = loader.load(self)
        assert image is not None
        self.__class__ = image.__class__
        self.__dict__ = image.__dict__
        return

    def _load(self):
        raise NotImplementedError('StubImageFile subclass must implement _load')


class _ParserFile:

    def __init__(self, data):
        self.data = data
        self.offset = 0

    def close(self):
        self.data = self.offset = None
        return

    def tell(self):
        return self.offset

    def seek(self, offset, whence=0):
        if whence == 0:
            self.offset = offset
        elif whence == 1:
            self.offset = self.offset + offset
        else:
            raise IOError('illegal argument to seek')

    def read(self, bytes=0):
        pos = self.offset
        if bytes:
            data = self.data[pos:pos + bytes]
        else:
            data = self.data[pos:]
        self.offset = pos + len(data)
        return data

    def readline(self):
        s = ''
        while 1:
            c = self.read(1)
            if not c:
                break
            s = s + c
            if c == '\n':
                break

        return s


class Parser:
    incremental = None
    image = None
    data = None
    decoder = None
    finished = 0

    def reset(self):
        assert self.data is None, 'cannot reuse parsers'
        return

    def feed(self, data):
        if self.finished:
            return
        else:
            if self.data is None:
                self.data = data
            else:
                self.data = self.data + data
            if self.decoder:
                if self.offset > 0:
                    skip = min(len(self.data), self.offset)
                    self.data = self.data[skip:]
                    self.offset = self.offset - skip
                    if self.offset > 0 or not self.data:
                        return
                (n, e) = self.decoder.decode(self.data)
                if n < 0:
                    self.data = None
                    self.finished = 1
                    if e < 0:
                        self.image = None
                        error = ERRORS.get(e, 'decoder error %d' % e)
                        raise IOError(error + ' when reading image file')
                    else:
                        return
                self.data = self.data[n:]
            elif self.image:
                pass
            try:
                try:
                    fp = _ParserFile(self.data)
                    im = Image.open(fp)
                finally:
                    fp.close()

            except IOError:
                pass
            else:
                flag = hasattr(im, 'load_seek') or hasattr(im, 'load_read')
                if flag or len(im.tile) != 1:
                    self.decode = None
                else:
                    im.load_prepare()
                    (d, e, o, a) = im.tile[0]
                    im.tile = []
                    self.decoder = Image._getdecoder(im.mode, d, a, im.decoderconfig)
                    self.decoder.setimage(im.im, e)
                    self.offset = o
                    if self.offset <= len(self.data):
                        self.data = self.data[self.offset:]
                        self.offset = 0
                self.image = im

            return

    def close(self):
        if self.decoder:
            self.feed('')
            self.data = self.decoder = None
            if not self.finished:
                raise IOError('image was incomplete')
        if not self.image:
            raise IOError('cannot parse this image')
        if self.data:
            try:
                fp = _ParserFile(self.data)
                self.image = Image.open(fp)
            finally:
                fp.close()

        return self.image


def _save(im, fp, tile):
    """Helper to save image based on tile list"""
    im.load()
    if not hasattr(im, 'encoderconfig'):
        im.encoderconfig = ()
    tile.sort(_tilesort)
    bufsize = max(MAXBLOCK, im.size[0] * 4)
    try:
        fh = fp.fileno()
        fp.flush()
    except AttributeError:
        for (e, b, o, a) in tile:
            e = Image._getencoder(im.mode, e, a, im.encoderconfig)
            if o > 0:
                fp.seek(o, 0)
            e.setimage(im.im, b)
            while 1:
                (l, s, d) = e.encode(bufsize)
                fp.write(d)
                if s:
                    break

            if s < 0:
                raise IOError('encoder error %d when writing image file' % s)

    else:
        for (e, b, o, a) in tile:
            e = Image._getencoder(im.mode, e, a, im.encoderconfig)
            if o > 0:
                fp.seek(o, 0)
            e.setimage(im.im, b)
            s = e.encode_to_file(fh, bufsize)
            if s < 0:
                raise IOError('encoder error %d when writing image file' % s)

        try:
            fp.flush()
        except:
            pass


def _safe_read(fp, size):
    if size <= 0:
        return ''
    if size <= SAFEBLOCK:
        return fp.read(size)
    data = []
    while size > 0:
        block = fp.read(min(size, SAFEBLOCK))
        if not block:
            break
        data.append(block)
        size = size - len(block)

    return string.join(data, '')