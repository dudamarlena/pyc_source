# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/newmovies.py
# Compiled at: 2008-08-28 14:30:02
import chunk, numpy as num, struct, wx, os
from params import params
from draw import annotate_bmp
__version__ = '0.3b'
import FlyMovieFormat as fmf
try:
    from FlyMovieFormat import NoMoreFramesException
except ImportError:

    class NoMoreFramesException(Exception):
        pass


class Movie():
    """Generic interface for all supported movie types.
    Also makes reading movies thread-safe."""

    def __init__(self, filename, interactive):
        """Figure out file type and initialize reader."""
        self.interactive = interactive
        (tmp, ext) = os.path.splitext(filename)
        if ext == '.fmf':
            self.type = 'fmf'
            try:
                self.h_mov = fmf.FlyMovie(filename)
            except NameError:
                if self.interactive:
                    wx.MessageBox('Couldn\'t open "%s"\n(maybe FMF is not installed?)' % filename, 'Error', wx.ICON_ERROR)
                raise
            except IOError:
                if self.interactive:
                    wx.MessageBox('I/O error opening "%s"' % filename, 'Error', wx.ICON_ERROR)
                raise

        elif ext == '.sbfmf':
            self.type = 'sbfmf'
            try:
                self.h_mov = fmf.FlyMovie(filename)
            except NameError:
                if self.interactive:
                    wx.MessageBox('Couldn\'t open "%s"\n(maybe FMF is not installed?)' % filename, 'Error', wx.ICON_ERROR)
                raise
            except IOError:
                if self.interactive:
                    wx.MessageBox('I/O error opening "%s"' % filename, 'Error', wx.ICON_ERROR)
                raise

        elif ext == '.avi':
            self.type = 'avi'
            try:
                self.h_mov = Avi(filename)
            except (TypeError, ValueError, AssertionError):
                if self.interactive:
                    wx.MessageBox('Failed opening file "%s".\nMake sure file is uncompressed, and either grayscale or RGB.' % filename, 'Error', wx.ICON_ERROR)
                raise
            else:
                if self.h_mov.bits_per_pixel == 24:
                    wx.MessageBox('Currently, RGB movies are immediately converted to grayscale. All color information is ignored.', 'Warning', wx.ICON_WARNING)
        else:
            if self.interactive:
                wx.MessageBox('Unknown file type %s' % filename[-4:], 'Error', wx.ICON_ERROR)
            raise TypeError('unknown file type %s' % filename[-4:])

    def get_frame(self, framenumber):
        """Return numpy array containing frame data."""
        try:
            try:
                (frame, stamp) = self.h_mov.get_frame(framenumber)
            except (IndexError, NoMoreFramesException):
                if self.interactive:
                    wx.MessageBox('Frame number %d out of range' % framenumber, 'Error', wx.ICON_ERROR)
                raise
            except (ValueError, AssertionError):
                if self.interactive:
                    wx.MessageBox('Error reading frame %d' % framenumber, 'Error', wx.ICON_ERROR)
                raise
            else:
                return (
                 frame, stamp)

        finally:
            pass

    def get_n_frames(self):
        return self.h_mov.get_n_frames()

    def get_width(self):
        return self.h_mov.get_width()

    def get_height(self):
        return self.h_mov.get_height()

    def get_some_timestamps(self, t1=0, t2=num.inf):
        t2 = min(t2, self.get_n_frames())
        timestamps = self.h_mov.get_all_timestamps()
        timestamps = timestamps[t1:t2]
        return timestamps

    def writesbfmf_start(self, bg, filename):
        self.nframescompress = self.get_n_frames() - params.start_frame
        self.writesbfmf_framestarts = num.zeros(self.nframescompress)
        self.writesbfmf_outfilename = filename
        self.outfile = open(self.writesbfmf_outfilename, 'wb')
        self.writesbfmf_writeheader(bg)

    def writesbfmf_isopen(self):
        if self.outfile is None:
            return False
        return not self.outfile.closed

    def writesbfmf_restart(self, frame, bg, filename):
        self.outfile = None
        self.writesbfmf_outfilename = filename
        self.nframescompress = self.get_n_frames() - params.start_frame
        self.writesbfmf_framestarts = num.zeros(self.nframescompress)
        tmpfilename = 'tmp_mtrax_writesbfmf.sbfmf'
        os.rename(filename, tmpfilename)
        inmovie = Movie(tmpfilename, self.interactive)
        self.outfile = open(filename, 'wb')
        self.writesbfmf_writeheader(bg)
        i = frame - params.start_frame - 1
        firstaddr = inmovie.h_mov.framelocs[0]
        lastaddr = inmovie.h_mov.framelocs[i]
        self.writesbfmf_framestarts[:(i + 1)] = inmovie.h_mov.framelocs[:i + 1]
        print 'copied framestarts: '
        print str(self.writesbfmf_framestarts[:i + 1])
        inmovie.h_mov.seek(0)
        pagesize = int(1048576)
        for j in range(firstaddr, lastaddr, pagesize):
            print 'writing page at %d' % inmovie.h_mov.file.tell()
            buf = inmovie.h_mov.read_some_bytes(pagesize)
            self.outfile.write(buf)

        if j < lastaddr:
            print 'writing page at %d' % inmovie.h_mov.file.tell()
            buf = inmovie.h_mov.read_some_bytes(int(lastaddr - pagesize))
            self.outfile.write(buf)
        inmovie.h_mov.close()
        os.remove(tmpfilename)
        return

    def writesbfmf_close(self, frame):
        self.writesbfmf_writeindex(frame)
        self.outfile.close()

    def writesbfmf_writeindex(self, frame):
        """
        Writes the index at the end of the file. Index consists of nframes unsigned long longs (Q),
        indicating the positions of each frame
        """
        indexloc = self.outfile.tell()
        nframeswrite = frame - params.start_frame + 1
        print 'writing index, nframeswrite = %d' % nframeswrite
        for i in range(nframeswrite):
            self.outfile.write(struct.pack('<Q', self.writesbfmf_framestarts[i]))

        self.outfile.seek(self.writesbfmf_indexptrloc)
        self.outfile.write(struct.pack('<Q', indexloc))
        self.outfile.seek(self.writesbfmf_nframesloc)
        self.outfile.write(struct.pack('<I', nframeswrite))

    def writesbfmf_writeheader(self, bg):
        """
        Writes the header for the file. Format:
        Number of bytes in version string: (I = unsigned int)
        Version Number (string of specified length)
        Number of rows (I = unsigned int)
        Number of columns (I = unsigned int)
        Number of frames (I = unsigned int)
        Difference mode (I = unsigned int):
          0 if light flies on dark background, unsigned mode
          1 if dark flies on light background, unsigned mode
          2 if other, signed mode
        Location of index (Q = unsigned long long)
        Background image (ncols * nrows * double)
        Standard deviation image (ncols * nrows * double)
        """
        self.nr = self.get_height()
        self.nc = self.get_width()
        if params.bg_type == params.BG_TYPE_LIGHTONDARK:
            difference_mode = 0
        elif params.bg_type == params.BG_TYPE_DARKONLIGHT:
            difference_mode = 1
        else:
            difference_mode = 2
        self.outfile.write(struct.pack('<I', len(__version__)))
        self.outfile.write(__version__)
        self.outfile.write(struct.pack('<2I', int(self.nr), int(self.nc)))
        self.writesbfmf_nframesloc = self.outfile.tell()
        self.outfile.write(struct.pack('<2I', int(self.nframescompress), int(difference_mode)))
        print 'writeheader: nframescompress = ' + str(self.nframescompress)
        stdloc = self.outfile.tell() + struct.calcsize('B') * self.nr * self.nc
        ffloc = stdloc + struct.calcsize('d') * self.nr * self.nc
        self.writesbfmf_indexptrloc = self.outfile.tell()
        self.outfile.write(struct.pack('<Q', 0))
        self.outfile.write(bg.center)
        self.outfile.write(bg.dev)

    def writesbfmf_writeframe(self, isfore, im, stamp, currframe):
        print 'writing frame %d' % currframe
        tmp = isfore.copy()
        tmp.shape = (self.nr * self.nc,)
        (i,) = num.nonzero(tmp)
        v = im[isfore]
        n = len(i)
        j = currframe - params.start_frame
        self.writesbfmf_framestarts[j] = self.outfile.tell()
        print 'stored in framestarts[%d]' % j
        self.outfile.write(struct.pack('<Id', n, stamp))
        i = i.astype(num.uint32)
        self.outfile.write(i)
        self.outfile.write(v)


class Avi():
    """Read uncompressed AVI movies."""

    def __init__(self, filename, fmfmode=False):
        self.fmfmode = fmfmode
        self.file = open(filename, 'rb')
        print 'avi'
        self.read_header()
        self.filename = filename
        self.chunk_start = self.data_start
        self.timestamp_len = 8
        if hasattr(self, 'newwidth'):
            self.bytes_per_chunk = self.height * self.newwidth + self.timestamp_len
        else:
            self.bytes_per_chunk = self.buf_size + self.timestamp_len

    def read_header(self):
        (RIFF, riff_size, AVI) = struct.unpack('4sI4s', self.file.read(12))
        if not RIFF == 'RIFF':
            raise TypeError('Invalid AVI file. Must be a RIFF file.')
        if not AVI == 'AVI ':
            raise TypeError('Invalid AVI file. File type must be AVI .')
        (LIST, hdrl_size, hdrl) = struct.unpack('4sI4s', self.file.read(12))
        hdrlstart = self.file.tell() - 4
        if not LIST == 'LIST' or not hdrl == 'hdrl':
            raise TypeError('Invalid AVI file. Did not find header list. %s should = LIST and %s should = hdrl' % (LIST, hdrl))
        (avih, avih_size) = struct.unpack('4sI', self.file.read(8))
        if not avih == 'avih':
            raise TypeError('Invalid AVI file. Did not find avi header.')
        avihchunkstart = self.file.tell()
        (self.frame_delay_us,) = struct.unpack('I', self.file.read(4))
        self.file.seek(12, 1)
        (self.n_frames,) = struct.unpack('I', self.file.read(4))
        self.file.seek(12, 1)
        (self.width, self.height) = struct.unpack('2I', self.file.read(8))
        self.file.seek(avihchunkstart + avih_size, 0)
        (LIST, stream_listsize, strl) = struct.unpack('4sI4s', self.file.read(12))
        if not LIST == 'LIST' or not strl == 'strl':
            raise TypeError('Invalid AVI file. Did not find stream list.')
        (strh, strh_size) = struct.unpack('4sI', self.file.read(8))
        if not strh == 'strh':
            raise TypeError('Invalid AVI file. Did not find stream header.')
        strhstart = self.file.tell()
        (vids, fcc) = struct.unpack('4s4s', self.file.read(8))
        if not vids == 'vids':
            raise TypeError('Unsupported AVI file type. First stream found is not a video stream.')
        print 'fcc[0] = >' + str(fcc[0]) + '<'
        print 'fcc[0] == <space> = ' + str(fcc[0] == ' ')
        print 'fcc = >%s<' % fcc
        print 'fcc == RGB = ' + str(fcc == ' RGB')
        if fcc not in ('DIB ', '\x00\x00\x00\x00', '', 'RAW ', 'NONE', ' RGB'):
            raise TypeError('Unsupported AVI file type %s, only uncompressed AVIs supported.' % fcc)
        self.file.seek(strhstart + strh_size, 0)
        (strf, strf_size) = struct.unpack('4sI', self.file.read(8))
        if not strf == 'strf':
            raise TypeError('Invalid AVI file. Did not find strf.')
        strfstart = self.file.tell()
        (bitmapheadersize,) = struct.unpack('I', self.file.read(4))
        self.file.seek(10, 1)
        (self.bits_per_pixel,) = struct.unpack('H', self.file.read(2))
        colormapsize = (strf_size - bitmapheadersize) / 4
        if colormapsize > 0:
            self.isindexed = True
            self.file.seek(strfstart + bitmapheadersize, 0)
            self.colormap = num.frombuffer(self.file.read(4 * colormapsize), num.uint8)
            self.colormap = self.colormap.reshape((colormapsize, 4))
            self.colormap = self.colormap[:, :-1]
        self.file.seek(hdrlstart + hdrl_size, 0)
        (LIST, movilist_size) = struct.unpack('4sI', self.file.read(8))
        if LIST == 'JUNK':
            self.file.seek(movilist_size, 1)
            (LIST, movilist_size) = struct.unpack('4sI', self.file.read(8))
        movistart = self.file.tell()
        if not LIST == 'LIST':
            raise TypeError('Invalid AVI file. Did not find movie LIST.')
        (movi,) = struct.unpack('4s', self.file.read(4))
        if not movi == 'movi':
            raise TypeError('Invalid AVI file. Did not find movi.')
        self.data_start = self.file.tell()
        (this_frame_id, frame_size) = struct.unpack('4sI', self.file.read(8))
        if not self.width * self.height * self.bits_per_pixel / 8 == frame_size:
            raise TypeError('Invalid AVI file. Frame size does not match width * height * bytesperpixel.')
        if self.isindexed:
            self.format = 'INDEXED'
        elif self.bits_per_pixel == 8:
            self.format = 'MONO8'
        elif self.bits_per_pixel == 24:
            self.format = 'RGB'
        else:
            raise TypeError('Unsupported AVI type. bitsperpixel must be 8 or 24, not %d.' % self.bits_per_pixel)
        self.buf_size = self.width * self.height * self.bits_per_pixel / 8

    def old_read_header(self):
        print 'reading chunk header'
        (file_type, riff_size) = struct.unpack('4sI', self.file.read(8))
        assert file_type == 'RIFF'
        stream_type = self.file.read(4)
        assert stream_type == 'AVI '
        (header_list, header_listsize, header_listtype) = struct.unpack('4sI4s', self.file.read(12))
        assert header_list == 'LIST' and header_listtype == 'hdrl'
        (avi_str, avi_note) = struct.unpack('4sI', self.file.read(8))
        assert avi_str == 'avih'
        print '1'
        avi_header = self.file.read(56)
        (self.frame_delay_us, AVI_data_rate, padding_size, AVI_flags, self.n_frames, n_preview_streams, n_data_streams, avi_buf_size, self.width, self.height, self.time_scale, self.data_rate, self.start_time, self.AVI_chunk_size) = struct.unpack('14I', avi_header)
        if n_data_streams != 1:
            raise TypeError('file must contain only one data stream')
        if avi_buf_size != 0:
            self.buf_size = avi_buf_size
        print '2'
        (stream_list, stream_listsize, stream_listtype) = struct.unpack('4sI4s', self.file.read(12))
        assert stream_list == 'LIST' and stream_listtype == 'strl'
        (stream_str, stream_note) = struct.unpack('4sI', self.file.read(8))
        assert stream_str == 'strh'
        stream_header = self.file.read(56)
        (fccType, fccHandler, stream_flags, priority, frames_interleave, stream_scale, stream_rate, stream_start, stream_length, stream_buf_size, stream_quality, stream_sample_size, x, y, w, h) = struct.unpack('4s4s10I4H', stream_header)
        print '3'
        if fccType != 'vids':
            raise TypeError('stream type must be video')
        if fccHandler not in ('DIB ', '\x00\x00\x00\x00', ''):
            print 'video must be uncompressed; found fccHandler %s' % fccHandler
            raise ValueError('video must be uncompressed; found fccHandler %s' % fccHandler)
        print 'stream_buf_size = ' + str(stream_buf_size)
        if stream_buf_size != 0:
            if hasattr(self, 'buf_size'):
                print 'buf_size = %d should = stream_buf_size = %d' % (self.buf_size, stream_buf_size)
                assert self.buf_size == stream_buf_size
            else:
                self.buf_size = stream_buf_size
        print '3.5'
        (bmp_str, bmp_note) = struct.unpack('4sI', self.file.read(8))
        print 'bmp_str = ' + str(bmp_str)
        assert bmp_str == 'strf'
        print '4'
        bmp_header = self.file.read(40)
        (self.bmp_size, bmp_width, bmp_height, bmp_planes, bmp_bitcount, crap, bmp_buf_size, xpels_per_meter, ypels_per_meter, color_used, color_important) = struct.unpack('I2i2H6i', bmp_header)
        assert bmp_width == self.width and bmp_height == self.height
        if bmp_buf_size != 0:
            if hasattr(self, 'buf_size'):
                assert self.buf_size == bmp_buf_size
            else:
                self.buf_size == stream_buf_size
        if not hasattr(self, 'buf_size'):
            self.buf_size = self.height * self.width
        print '5'
        movie_list = ''
        movie_listtype = ''
        while movie_list != 'LIST':
            s = ''
            EOF_flag = False
            while s.find('movi') < 0 and not EOF_flag:
                p = self.file.tell()
                s = self.file.read(128)
                if s == '':
                    EOF_flag = True

            if EOF_flag:
                break
            self.file.seek(p)
            self.file.read(s.find('movi') - 8)
            (movie_list, movie_listsize, movie_listtype) = struct.unpack('4sI4s', self.file.read(12))

        assert movie_list == 'LIST' and movie_listtype == 'movi'
        self.data_start = self.file.tell()
        print '6'
        (this_frame_id, frame_size) = struct.unpack('4sI', self.file.read(8))
        if frame_size == self.width * self.height:
            pass
        elif frame_size == 3 * self.width * self.height:
            raise TypeError('movie must be grayscale')
        elif frame_size % self.height == 0:
            self.newwidth = frame_size / self.height
            if abs(self.newwidth - self.width) > 10:
                raise ValueError('apparent new width = %d; expected width = %d' % (
                 self.height, self.newwidth))
        else:
            raise ValueError('apparent new width is not integral; mod = %d' % (frame_size % self.height))
        print '8'

    def get_frame(self, framenumber):
        """Read frame from file and return as NumPy array."""
        if framenumber < 0:
            raise IndexError
        if framenumber >= self.n_frames:
            raise NoMoreFramesException
        self.file.seek(self.data_start + (self.buf_size + 8) * framenumber)
        return self.get_next_frame()

    def get_next_frame(self):
        """returns next frame"""
        currentseekloc = self.file.tell()
        (this_frame_id, frame_size) = struct.unpack('4sI', self.file.read(8))
        if frame_size != self.buf_size:
            raise ValueError('Frame size does not equal buffer size; movie must be uncompressed')
        if not hasattr(self, 'frame_id'):
            self.frame_id = this_frame_id
        elif this_frame_id != self.frame_id:
            raise ValueError('error seeking frame start: unknown data header')
        frame_data = self.file.read(frame_size)
        frame = num.fromstring(frame_data, num.uint8)
        if self.isindexed:
            frame = self.colormap[frame, :]
            frame.resize((self.width, self.height, 3))
            tmp = frame.astype(float)
            tmp = tmp[:, :, 0] * 0.3 + tmp[:, :, 1] * 0.59 + tmp[:, :, 2] * 0.11
            frame = tmp.astype(num.uint8)
        elif frame.size == self.width * self.height:
            frame.resize((self.height, self.width))
        elif frame.size == self.width * self.height * 3:
            frame.resize((self.height, self.width, 3))
            tmp = frame.astype(float)
            tmp = tmp[:, :, 0] * 0.3 + tmp[:, :, 1] * 0.59 + tmp[:, :, 2] * 0.11
            frame = tmp.astype(num.uint8)
        elif frame.size % self.height == 0:
            self.newwidth = frame.size / self.height
            if abs(self.newwidth - self.width) < 10:
                frame.resize((self.newwidth, self.height))
            else:
                raise ValueError('apparent new width = %d; expected width = %d' % (
                 self.height, self.newwidth))
        else:
            raise ValueError('apparent new width is not integral; mod = %d' % (frame.size % self.height))
        framenumber = (currentseekloc - self.chunk_start) / self.bytes_per_chunk
        if self.frame_delay_us != 0:
            stamp = framenumber * self.frame_delay_us / 1000000.0
        elif self.time_scale != 0:
            stamp = framenumber * self.data_rate / float(self.time_scale)
        else:
            stamp = framenumber / 24
        if self.fmfmode:
            shape = frame.shape
            frame.shape = (shape[1], shape[0])
        return (frame, stamp)

    def get_n_frames(self):
        return self.n_frames

    def get_width(self):
        if hasattr(self, 'newwidth'):
            return self.newwidth
        else:
            return self.width

    def get_height(self):
        return self.height

    def seek(self, frame_number):
        if frame_number < 0:
            frame_number = self.n_frames + frame_number
        seek_to = self.chunk_start + self.bytes_per_chunk * frame_number
        self.file.seek(seek_to)


def write_results_to_avi(movie, tracks, filename, f0=None, f1=None):
    nframes = len(tracks)
    if f0 is None:
        f0 = params.start_frame
    if f1 is None:
        f1 = nframes + params.start_frame - 1
    f0 -= params.start_frame
    f1 -= params.start_frame
    f0 = max(0, min(nframes - 1, f0))
    f1 = max(0, min(nframes - 1, f1))
    nframes_write = f1 - f0 + 1
    outstream = open(filename, 'wb')
    write_avi_header(movie, tracks, filename, outstream, f0, f1)
    movilistloc = outstream.tell()
    offsets = num.zeros(nframes_write)
    for i in range(f0, f1 + 1):
        if i % 100 == 0:
            print 'Frame %d / %d' % (i, nframes_write)
        offsets[i - f0] = write_avi_frame(movie, tracks, i, outstream)

    offsets -= movilistloc + 4
    write_avi_index(movie, tracks, offsets, outstream, f0, f1)
    outstream.close()
    return


def write_avi_index(movie, tracks, offsets, outstream, f0, f1):
    nframes = f1 - f0 + 1
    idx1size = 8 + 16 * nframes
    BYTESPERPIXEL = 3
    bytesperframe = movie.get_width() * movie.get_height() * BYTESPERPIXEL
    write_chunk_header('idx1', idx1size, outstream)
    for i in range(len(offsets)):
        outstream.write(struct.pack('4s', '00db'))
        outstream.write(struct.pack('I', 16))
        outstream.write(struct.pack('I', offsets[i]))
        outstream.write(struct.pack('I', bytesperframe))


def write_avi_frame(movie, tracks, i, outstream):
    height = movie.get_height()
    width = movie.get_width()
    BYTESPERPIXEL = 3
    bytesperframe = width * height * BYTESPERPIXEL
    if tracks is None:
        return
    if i >= len(tracks):
        return
    j = params.start_frame + i
    try:
        (frame, last_timestamp) = movie.get_frame(j)
    except (IndexError, NoMoreFramesException):
        return

    ellipses = tracks[i]
    old_pts = []
    early_frame = int(max(0, i - params.tail_length))
    for dataframe in tracks[early_frame:i + 1]:
        these_pts = []
        for ellipse in dataframe.itervalues():
            these_pts.append((ellipse.center.x, ellipse.center.y,
             ellipse.identity))

        old_pts.append(these_pts)

    (bitmap, resize, img_size) = annotate_bmp(frame, ellipses, old_pts, params.ellipse_thickness, [
     height, width])
    img = bitmap.ConvertToImage()
    img = img.Mirror(True)
    img = img.GetData()
    outstream.write(struct.pack('4s', '00db'))
    outstream.write(struct.pack('I', bytesperframe))
    offset = outstream.tell()
    outstream.write(img[::-1])
    pad = bytesperframe % 2
    if pad == 1:
        outstream.write(struct.pack('B', 0))
    return offset


def write_avi_header(movie, tracks, filename, outstream, f0, f1):
    BYTESPERPIXEL = 3
    nframes = f1 - f0 + 1
    width = movie.get_width()
    height = movie.get_height()
    bytesperframe = width * height * BYTESPERPIXEL
    avihsize = 64
    strllistsize = 116
    strhsize = 56
    strfsize = 48
    hdrllistsize = avihsize + strllistsize + 12
    movilistsize = 12
    idx1size = 8
    riffsize = hdrllistsize + movilistsize + idx1size
    movilistsize += nframes * (8 + bytesperframe + bytesperframe % 2)
    idx1size += nframes * 16
    riffsize += nframes * (8 + bytesperframe + 16 + bytesperframe % 2)
    write_chunk_header('RIFF', riffsize, outstream)
    outstream.write(struct.pack('4s', 'AVI '))
    write_list_header('hdrl', hdrllistsize - 8, outstream)
    write_chunk_header('avih', avihsize - 8, outstream)
    if hasattr(movie, 'frame_delay_us'):
        microsecperframe = movie.frame_delay_us
    else:
        microsecperframe = estimate_frame_delay_us(movie.h_mov)
    outstream.write(struct.pack('I', int(round(microsecperframe))))
    framespersec = 1000000.0 / microsecperframe
    bytespersec = framespersec * bytesperframe
    outstream.write(struct.pack('I', int(num.ceil(bytespersec))))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('I', 16))
    outstream.write(struct.pack('I', nframes))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('I', 1))
    outstream.write(struct.pack('I', bytesperframe))
    outstream.write(struct.pack('I', width))
    outstream.write(struct.pack('I', height))
    outstream.write(struct.pack('2I', 100, 100 * framespersec))
    outstream.write(struct.pack('2I', 0, 0))
    write_list_header('strl', strllistsize - 8, outstream)
    write_chunk_header('strh', strhsize - 8, outstream)
    outstream.write(struct.pack('4s', 'vids'))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('2I', 100, 100 * framespersec))
    outstream.write(struct.pack('2I', 0, 0))
    outstream.write(struct.pack('I', bytesperframe))
    outstream.write(struct.pack('I', 7500))
    outstream.write(struct.pack('I', 0))
    write_chunk_header('strf', strfsize - 8, outstream)
    outstream.write(struct.pack('I', 40))
    outstream.write(struct.pack('I', width))
    outstream.write(struct.pack('I', height))
    outstream.write(struct.pack('H', 1))
    outstream.write(struct.pack('H', 24))
    outstream.write(struct.pack('I', 0))
    outstream.write(struct.pack('I', bytesperframe))
    outstream.write(struct.pack('4I', 0, 0, 0, 0))
    write_list_header('movi', movilistsize, outstream)


def write_chunk_header(chunktype, chunksize, outstream):
    outstream.write(struct.pack('4sI', chunktype, chunksize))


def write_list_header(listtype, listsize, outstream):
    outstream.write(struct.pack('4sI4s', 'LIST', listsize, listtype))


def estimate_frame_delay_us(mov):
    if not hasattr(mov, 'chunk_start'):
        return 0
    if mov.issbfmf:
        return 50000.0
    else:
        mov.file.seek(mov.chunk_start)
        stamp0 = mov.get_next_timestamp()
        mov.file.seek(mov.chunk_start + mov.bytes_per_chunk * (mov.n_frames - 1))
        stamp1 = mov.get_next_timestamp()
        frame_delay_us = float(stamp1 - stamp0) / float(mov.n_frames - 1) * 1000000.0
        return frame_delay_us