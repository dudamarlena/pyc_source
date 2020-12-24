# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/movie.py
# Compiled at: 2011-03-28 15:09:52
import sys, zlib, re
from swf import SWFParser, FLVParser, CURSOR_DEPTH
from mp3 import MP3Reader, MP3Storage
from rfb import RFBMovieConverter
from image import IMG_LOSSLESS, IMG_VIDEOPACKET
import html_templates
stderr = sys.stderr
lowerbound = max
upperbound = min

class SWFInfo:
    """
  SWFInfo holds information about headers and mp3 data
  in a SWF file. The values of this object are changed
  as parsing goes on.
  """

    def __init__(self, filename=None):
        self.filename = filename
        self.compression = None
        self.clipping = None
        self.framerate = None
        self.scaling = None
        self.blocksize = None
        self.swf_version = None
        self.width = None
        self.height = None
        self.mp3 = None
        self.scalable = False
        return

    def __repr__(self):
        return '<SWFInfo: filename=%r, compression=%r, clipping=%r, framerate=%r, scaling=%r, blocksize=%r, swf_version=%r, mp3=%r>' % (
         self.filename, self.compression, self.clipping, self.framerate, self.scaling, self.blocksize, self.swf_version, self.mp3)

    def set_defaults(self, w0, h0):
        if not self.clipping:
            self.clipping = (
             0, 0, w0, h0)
        else:
            w0, h0 = self.clipping[2], self.clipping[3]
        if self.scaling:
            w0, h0 = int(w0 * self.scaling), int(h0 * self.scaling)
        if self.width != None and (self.width != w0 or self.height != h0):
            print >> stderr, 'Warning: movie size already set: %dx%d' % (self.width, self.height)
        elif self.width == None:
            self.width, self.height = w0, h0
            print >> stderr, 'Output movie size: %dx%d' % (self.width, self.height)
        if not self.framerate:
            self.framerate = 12.0
        if not self.blocksize:
            self.blocksize = 32
        return

    def set_scalable(self, scalable):
        self.scalable = scalable

    def set_framerate(self, framerate):
        if self.framerate != None and self.framerate != framerate:
            print >> stderr, 'Warning: movie framerate is overridden.'
            return
        else:
            self.framerate = float(framerate)
            return

    def set_clipping(self, s):
        m = re.match('^(\\d+)x(\\d+)\\+(\\d+)\\+(\\d+)$', s)
        if not m:
            raise ValueError('Invalid clipping spec: %r' % s)
        f = map(int, m.groups())
        self.clipping = (f[2], f[3], f[0], f[1])

    def get_clipping(self):
        if not self.clipping:
            raise ValueError('Clipping not set.')
        (x, y, w, h) = self.clipping
        return '%dx%d+%d+%d' % (w, h, x, y)

    def set_swf_version(self, swf_version):
        self.swf_version = swf_version

    def set_mp3header(self, isstereo, mp3samplerate, mp3sampleskip):
        if not self.mp3:
            self.mp3 = MP3Storage()
        self.mp3.set_stereo(isstereo)
        self.mp3.set_sample_rate(mp3samplerate)
        self.mp3.set_initial_skip(mp3sampleskip)
        print >> stderr, 'MP3: stereo=%s, samplerate=%d, initialskip=%d' % (isstereo, mp3samplerate, mp3sampleskip)

    def reg_mp3blocks(self, fp, length=None, nsamples=None, seeksamples=None):
        if not self.mp3:
            self.mp3 = MP3Storage()
        MP3Reader(self.mp3).read_mp3file(fp, length, nsamples, seeksamples)

    def write_html(self, seekbar=True, loop=True, filename=None):
        if not (self.swf_version and self.width and self.height):
            return
        if not filename:
            filename = self.filename
        if filename.endswith('.swf'):
            outfname = filename.replace('.swf', '.html')
        else:
            outfname = filename + '.html'
        print >> stderr, 'Writing: %s...' % outfname
        out = file(outfname, 'w')
        html_templates.generate_html(out, filename, seekbar=seekbar, loop=loop)
        out.close()


class MovieContainer:
    """
  MovieContainer holds all frame images of a movie.
  """

    def __init__(self, info):
        self.info = info
        self.nframes = 0
        self.parsers = []

    def get_frame(self, i):
        images, othertags, cursor_info = [], [], (None, None)
        for (n, parser) in self.parsers:
            if i < n:
                (images, othertags, cursor_info) = parser.parse_frame(i)
                break
            i -= n

        return (images, othertags, cursor_info)

    def parse_vnc2swf(self, fname, read_mp3=False, debug=0):
        parser = VNC2SWF_Parser(self, read_mp3, debug=debug)
        parser.open(fname)
        nframes = len(parser.framepos)
        self.parsers.append((nframes, parser))
        self.nframes += nframes
        return self

    def parse_flv(self, fname, read_mp3=False, debug=0):
        parser = FLVMovieParser(self, read_mp3, debug=debug)
        parser.open(fname)
        nframes = len(parser.frames)
        self.parsers.append((nframes, parser))
        self.nframes += nframes
        return self

    def parse_vncrec(self, fname, debug=0):
        parser = RFBMovieConverter(self, debug=debug)
        parser.open(fname)
        nframes = len(parser.frameinfo)
        self.parsers.append((nframes, parser))
        self.nframes += nframes
        return self


class VNC2SWF_Parser(SWFParser):
    """
  VNC2SWF_Parser parses a SWF file which is specifically
  created by vnc2swf. This does not support a generic
  Flash file.
  """

    def __init__(self, movie, read_mp3=False, debug=0):
        SWFParser.__init__(self, debug)
        self.movie = movie
        self.read_mp3 = read_mp3
        self.video1_cid = None
        return

    def parse_header(self):
        SWFParser.parse_header(self)
        (x, width, y, height) = self.rect
        print >> stderr, 'Input movie: version=%d, size=%dx%d, framerate=%dfps, frames=%d, duration=%.1fs.' % (
         self.swf_version, width / 20, height / 20, self.framerate,
         self.framecount, self.framecount / float(self.framerate))
        self.movie.info.set_framerate(self.framerate)
        self.movie.info.set_defaults(width / 20, height / 20)

    def parse_frame(self, i):
        self.image1 = {}
        self.shape1 = None
        self.images = []
        self.othertags = []
        self.cursor_image = None
        self.cursor_pos = None
        SWFParser.parse_frame(self, i)
        return (
         self.images, self.othertags, (self.cursor_image, self.cursor_pos))

    def do_tag0(self, tag, length):
        pass

    def do_unknown_tag(self, tag, length):
        data = self.read(length)
        self.othertags.append((tag, data))

    def do_tag1(self, tag, length):
        if self.debug:
            print >> stderr, 'ShowFrame'

    def do_tag9(self, tag, length):
        bgcolor = self.readrgb()
        if self.debug:
            print >> stderr, 'BGColor:', bgcolor

    def do_tag20(self, tag, length):
        cid = self.readui16()
        fmt = self.readui8()
        width = self.readui16()
        height = self.readui16()
        length -= 7
        tablesize = 0
        if fmt == 3:
            tablesize = self.readui8() + 1
            length -= 1
        if fmt == 5:
            data = self.read(length)
            if self.debug:
                print >> stderr, 'DefineBitsLossless:', cid, fmt, width, height, len(data)
            self.image1[cid] = (
             width, height, (IMG_LOSSLESS, data))

    do_tag36 = do_tag20

    def do_tag32(self, tag, length):
        sid = self.readui16()
        rect = self.readrect()
        (fillstyles, linestyles) = self.read_style(3)
        shape = self.read_shape(3, fillstyles, linestyles)
        if fillstyles:
            cid = fillstyles[0][3]
            if self.debug:
                print >> stderr, 'Shape', sid, cid, rect, shape, fillstyles, linestyles
            self.shape1 = (
             sid, cid)

    def do_tag26(self, tag, length):
        flags = self.readui8()
        depth = self.readui16()
        (sid, ratio, name) = (None, None, None)
        (scalex, scaley, rot0, rot1, transx, transy) = (None, None, None, None, None,
                                                        None)
        if flags & 2:
            sid = self.readui16()
        if flags & 4:
            (scalex, scaley, rot0, rot1, transx, transy) = self.readmatrix()
        if flags & 16:
            ratio = self.readui16()
        if flags & 32:
            name = self.readstring()
        if self.debug:
            print >> stderr, 'Place', flags, depth, sid, (scalex, scaley, rot0, rot1, transx, transy)
        if depth == CURSOR_DEPTH:
            if sid:
                (sid0, cid) = self.shape1
                if sid0 == sid and cid in self.image1:
                    (width, height, (t, data)) = self.image1[cid]
                    self.cursor_image = (width, height, 0, 0, zlib.decompress(data))
            if transx != None:
                self.cursor_pos = (
                 transx / 20, transy / 20)
        elif not sid or sid == self.video1_cid:
            pass
        elif self.shape1 and transx != None:
            (sid0, cid) = self.shape1
            if sid0 == sid and cid in self.image1:
                data = self.image1[cid]
                del self.image1[cid]
                self.images.append(((transx / 20, transy / 20), data))
                self.shape1 = None
        return

    def do_tag28(self, tag, length):
        depth = self.readui16()
        if self.debug:
            print >> stderr, 'RemoveObject', depth

    def scan_tag60(self, tag, length):
        if self.video1_cid:
            print >> stderr, 'DefineVideoStream already appeared.'
            return
        cid = self.readui16()
        frames = self.readui16()
        width = self.readui16()
        height = self.readui16()
        flags = self.readui8()
        codec = self.readui8()
        if codec == 3:
            self.video1_cid = cid
            if self.debug:
                print >> stderr, 'DefineVideoStream', cid, frames, width, height, flags, codec

    def do_tag60(self, tag, length):
        pass

    def do_tag61(self, tag, length):
        stream_id = self.readui16()
        if self.video1_cid != stream_id:
            return
        framenum = self.readui16()
        self.setbuff()
        frametype, codecid = self.readbits(4), self.readbits(4)
        if codecid != 3:
            return
        blockwidth, imagewidth = self.readbits(4), self.readbits(12)
        blockheight, imageheight = self.readbits(4), self.readbits(12)
        blockwidth = (blockwidth + 1) * 16
        blockheight = (blockheight + 1) * 16
        if self.debug:
            print >> stderr, 'VideoFrame', framenum, frametype, ':', blockwidth, imagewidth, blockheight, imageheight
        hblocks = (imagewidth + blockwidth - 1) / blockwidth
        vblocks = (imageheight + blockheight - 1) / blockheight
        for y in xrange(0, vblocks):
            for x in xrange(0, hblocks):
                length = self.readub16()
                if length:
                    data = self.read(length)
                    x0 = x * blockwidth
                    y0 = imageheight - (y + 1) * blockheight
                    w = upperbound(blockwidth, imagewidth - x0)
                    h = blockheight
                    if y0 < 0:
                        h += y0
                        y0 = 0
                    self.images.append(((x0, y0), (w, h, (IMG_VIDEOPACKET, data))))

    def scan_tag18(self, tag, length):
        if not self.read_mp3:
            return
        flags1 = self.readui8()
        flags2 = self.readui8()
        playrate = (flags1 & 12) >> 2
        if not flags1 & 2:
            return
        playstereo = flags1 & 1
        compression = (flags2 & 240) >> 4
        if compression != 2:
            return
        samplerate = (flags2 & 12) >> 2
        if samplerate == 0:
            return
        samplerate = [
         0, 11025, 22050, 44100][samplerate]
        if not flags2 & 2:
            return
        streamstereo = flags2 & 1
        avgsamplecount = self.readui16()
        latseek = self.readui16()
        self.movie.info.set_mp3header(streamstereo, samplerate, latseek)
        if self.debug:
            print >> stderr, 'SoundStreamHeader', flags1, flags2, avgsamplecount, latseek

    def do_tag18(self, tag, length):
        pass

    def scan_tag19(self, tag, length):
        if not self.read_mp3:
            return
        nsamples = self.readui16()
        seeksamples = self.readsi16()
        self.movie.info.reg_mp3blocks(self.fp, length - 4, nsamples, seeksamples)
        if self.debug:
            print >> stderr, 'SoundStreamBlock', nsamples, seeksamples

    def do_tag19(self, tag, length):
        pass


class FLVMovieParser(FLVParser):

    def __init__(self, movie, read_mp3, debug=0):
        FLVParser.__init__(self, debug=debug)
        self.movie = movie
        self.read_mp3 = read_mp3
        self.framerate = 12

    def open(self, fname):
        FLVParser.open(self, fname)
        self.movie.info.set_framerate(self.framerate)
        for (tag, _, _, offset) in self.tags:
            if tag == 9:
                self.fp.seek(offset + 1)
                self.setbuff()
                _, imagewidth = self.readbits(4), self.readbits(12)
                _, imageheight = self.readbits(4), self.readbits(12)
                self.movie.info.set_defaults(imagewidth, imageheight)
                break

        self.frames = []
        tagids = []
        for (tagid, (_, _, t, _)) in enumerate(self.tags):
            if len(self.frames) * 1000 / self.framerate < t:
                self.frames.append(tagids)
                tagids = []
            tagids.append(tagid)

        self.frames.append(tagids)

    def parse_frame(self, i):
        self.images = []
        self.othertags = []
        for tagid in self.frames[i]:
            self.process_tag(tagid)

        return (self.images, self.othertags, (None, None))

    def process_tag(self, tagid):
        (tag, _, _, offset) = self.tags[tagid]
        if tag != 9:
            return
        self.fp.seek(offset)
        self.setbuff()
        frametype, codecid = self.readbits(4), self.readbits(4)
        if codecid != 3:
            return
        blockwidth, imagewidth = self.readbits(4), self.readbits(12)
        blockheight, imageheight = self.readbits(4), self.readbits(12)
        blockwidth = (blockwidth + 1) * 16
        blockheight = (blockheight + 1) * 16
        if self.debug:
            print >> stderr, 'VideoFrame', framenum, frametype, ':', blockwidth, imagewidth, blockheight, imageheight
        hblocks = (imagewidth + blockwidth - 1) / blockwidth
        vblocks = (imageheight + blockheight - 1) / blockheight
        for y in xrange(0, vblocks):
            for x in xrange(0, hblocks):
                length = self.readub16()
                if length:
                    data = self.read(length)
                    x0 = x * blockwidth
                    y0 = imageheight - (y + 1) * blockheight
                    w = upperbound(blockwidth, imagewidth - x0)
                    h = blockheight
                    if y0 < 0:
                        h += y0
                        y0 = 0
                    self.images.append(((x0, y0), (w, h, (IMG_VIDEOPACKET, data))))


if __name__ == '__main__':
    info = SWFInfo()
    movie = MovieContainer(info).parse_vnc2swf(sys.argv[1], read_mp3=True, debug=1)
    print movie.nframes, info