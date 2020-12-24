# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/movies.py
# Compiled at: 2016-09-17 17:03:48
import chunk, multiprocessing, os, struct, sys, traceback, cv2, numpy as num, wx
from params import params
from ellipsesk import annotate_bmp
__version__ = '0.3b'
import FlyMovieFormat as fmf
try:
    from FlyMovieFormat import NoMoreFramesException
except ImportError:

    class NoMoreFramesException(Exception):
        pass


try:
    import ufmf
except ImportError:
    pass

DEBUG_MOVIES = True
from version import DEBUG
if not DEBUG:
    DEBUG_MOVIES = False

def known_extensions():
    return [
     '.fmf', '.avi', '.sbfmf', '.ufmf']


class Movie():
    """Generic interface for all supported movie types."""

    def __init__(self, initpath, interactive=True, parentframe=None, open_now=True, open_multiple=False, default_extension='.fmf'):
        """Prepare to open a movie (awaiting call to self.open()).
If initpath is a filename, just use it.
If initpath is a directory and interactive is True, then ask user for a filename.
If initpath is a directory and not in interactive mode, it's an error."""
        self.interactive = interactive
        self.dirname = ''
        self.filename = ''
        self.fullpath = ''
        if os.path.isfile(initpath):
            self.fullpath = initpath
            self.dirname, self.filename = os.path.split(self.fullpath)
        elif self.interactive:
            extensions = {'.fmf': 'fly movie format files (*.fmf)', '.avi': 'audio-video interleave files (*.avi)', 
               '.sbfmf': 'static background fly movie format files (*.sbfmf)', 
               '.ufmf': 'micro fly movie format files (*.ufmf)'}
            if len(known_extensions()) != len(extensions):
                print "movie-open dialog doesn't list the same number of extensions as known_extensions()"
            dialog_str = ''
            if default_extension in extensions.keys():
                dialog_str = extensions[default_extension] + '|*' + default_extension + '|'
                del extensions[default_extension]
            for ext, txt in extensions.iteritems():
                dialog_str += txt + '|*' + ext + '|'

            dialog_str += 'Any (*)|*'
            flags = wx.FD_OPEN
            if open_multiple:
                flags = wx.FD_OPEN | wx.FD_MULTIPLE
            dlg = wx.FileDialog(parentframe, 'Select movie', initpath, '', dialog_str, flags)
            if dlg.ShowModal() == wx.ID_OK:
                if open_multiple:
                    paths = dlg.GetPaths()
                    if len(paths) == 1:
                        self.fullpath = paths[0]
                    else:
                        self.fullpaths_mult = paths
                        self.fullpath = paths[0]
                else:
                    self.fullpath = dlg.GetPath()
                self.dirname, self.filename = os.path.split(self.fullpath)
            else:
                raise ImportError('no filename was selected')
            dlg.Destroy()
        else:
            raise ValueError("not in interactive mode but wasn't given a full filename, or file not found at " + initpath)
        if open_now:
            self.open()

    def open(self):
        """Figure out file type and initialize reader."""
        print 'Opening video ' + self.fullpath
        front, ext = os.path.splitext(self.fullpath)
        ext = ext.lower()
        if ext not in known_extensions():
            print 'unknown file extension; will try OpenCV to open'
        if ext == '.fmf':
            self.type = 'fmf'
            try:
                self.h_mov = fmf.FlyMovie(self.fullpath)
            except NameError:
                if self.interactive:
                    wx.MessageBox('Couldn\'t open "%s"\n(maybe FMF is not installed?)' % filename, 'Error', wx.ICON_ERROR | wx.OK)
                raise
            except IOError:
                if self.interactive:
                    wx.MessageBox('I/O error opening "%s"' % self.fullpath, 'Error', wx.ICON_ERROR | wx.OK)
                raise

        elif ext == '.sbfmf':
            self.type = 'sbfmf'
            try:
                self.h_mov = fmf.FlyMovie(self.fullpath)
            except NameError:
                if self.interactive:
                    wx.MessageBox('Couldn\'t open "%s"\n(maybe FMF is not installed?)' % filename, 'Error', wx.ICON_ERROR | wx.OK)
                raise
            except IOError:
                if self.interactive:
                    wx.MessageBox('I/O error opening "%s"' % self.fullpath, 'Error', wx.ICON_ERROR | wx.OK)
                raise

        elif ext == '.ufmf':
            self.type = 'ufmf'
            try:
                self.h_mov = ufmf.FlyMovieEmulator(self.fullpath)
            except NameError:
                if self.interactive:
                    wx.MessageBox('Couldn\'t open "%s"\n(maybe UFMF is not installed?)' % filename, 'Error', wx.ICON_ERROR | wx.OK)
                raise
            except IOError:
                if self.interactive:
                    wx.MessageBox('I/O error opening "%s"' % self.fullpath, 'Error', wx.ICON_ERROR | wx.OK)
                raise
            except ufmf.ShortUFMFFileError:
                if self.interactive:
                    wx.MessageBox('Error opening "%s". Short ufmf file.' % filename, 'Error', wx.ICON_ERROR | wx.OK)
                raise
            except ufmf.CorruptIndexError:
                if self.interactive:
                    wx.MessageBox('Error opening "%s". Corrupt file index.' % filename, 'Error', wx.ICON_ERROR | wx.OK)
                raise
            except ufmf.InvalidMovieFileException:
                if self.interactive:
                    wx.MessageBox('Error opening "%s". Invalid movie file.' % filename, 'Error', wx.ICON_ERROR | wx.OK)
                raise

        elif ext == '.avi':
            try:
                if not params.use_uncompressed_avi:
                    if DEBUG:
                        print 'Not using uncompressed AVI class'
                    raise
                self.h_mov = Avi(self.fullpath)
                self.type = 'avi'
            except:
                try:
                    self.h_mov = CompressedAvi(self.fullpath)
                    self.type = 'cavi'
                except Exception as details:
                    if self.interactive:
                        msgtxt = 'Failed opening file "%s".' % self.fullpath
                        wx.MessageBox(msgtxt, 'Error', wx.ICON_ERROR | wx.OK)
                    raise
                else:
                    print 'reading compressed AVI'

            if self.interactive and self.h_mov.bits_per_pixel == 24 and not DEBUG_MOVIES and False:
                wx.MessageBox('Currently, RGB movies are immediately converted to grayscale. All color information is ignored.', 'Warning', wx.ICON_WARNING | wx.OK)
        else:
            try:
                self.h_mov = CompressedAvi(self.fullpath)
                self.type = 'cavi'
            except:
                if self.interactive:
                    wx.MessageBox('Failed opening file "%s".' % self.fullpath, 'Error', wx.ICON_ERROR | wx.OK)
                raise

            if self.interactive:
                wx.MessageBox('Ctrax is assuming your movie is in an AVI format and is most likely compressed. Out-of-order frame access (e.g. dragging the frame slider toolbars around) will be slow. At this time, the frame chosen to be displayed may be off by one or two frames, i.e. may not line up perfectly with computed trajectories.', 'Warning', wx.ICON_WARNING | wx.OK)
            else:
                print 'reading movie as compressed AVI'
        self.file_lock = multiprocessing.RLock()
        self.bufferedframe_im = None
        self.bufferedframe_stamp = None
        self.bufferedframe_num = None
        return

    def is_open(self):
        return hasattr(self, 'h_mov')

    def close(self):
        """Close the movie file."""
        del self.file_lock
        del self.h_mov
        del self.type

    def get_frame(self, framenumber):
        """Return numpy array containing frame data."""
        if framenumber == self.bufferedframe_num:
            return (self.bufferedframe_im.copy(), self.bufferedframe_stamp)
        with self.file_lock:
            try:
                frame, stamp = self.h_mov.get_frame(framenumber)
            except (IndexError, NoMoreFramesException):
                if self.interactive:
                    wx.MessageBox('Frame number %d out of range' % framenumber, 'Error', wx.ICON_ERROR | wx.OK)
                else:
                    print 'frame', framenumber, 'out of range'
                raise
            except (ValueError, AssertionError):
                if self.interactive:
                    wx.MessageBox('Error reading frame %d' % framenumber, 'Error', wx.ICON_ERROR | wx.OK)
                else:
                    print 'error reading frame', framenumber
                raise
            else:
                if params.movie_flipud:
                    frame = num.flipud(frame)
                self.bufferedframe_im = frame.copy()
                self.bufferedframe_stamp = stamp
                self.bufferedframe_num = framenumber
                return (
                 frame, stamp)

    def get_n_frames(self):
        with self.file_lock:
            return self.h_mov.get_n_frames()

    def get_width(self):
        with self.file_lock:
            return self.h_mov.get_width()

    def get_height(self):
        with self.file_lock:
            return self.h_mov.get_height()

    def get_some_timestamps(self, t1=0, t2=num.inf):
        with self.file_lock:
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
        if not hasattr(self, 'outfile') or self.outfile is None:
            return False
        return not self.outfile.closed

    def writesbfmf_restart(self, frame, bg, filename):
        self.outfile = None
        self.writesbfmf_outfilename = filename
        self.nframescompress = self.get_n_frames() - params.start_frame
        self.writesbfmf_framestarts = num.zeros(self.nframescompress)
        tmpfilename = 'tmp_ctrax_writesbfmf.sbfmf'
        os.rename(filename, tmpfilename)
        inmovie = Movie(tmpfilename, self.interactive)
        self.outfile = open(filename, 'wb')
        self.writesbfmf_writeheader(bg)
        i = frame - params.start_frame - 1
        firstaddr = inmovie.h_mov.framelocs[0]
        lastaddr = inmovie.h_mov.framelocs[i]
        self.writesbfmf_framestarts[:(i + 1)] = inmovie.h_mov.framelocs[:i + 1]
        if DEBUG_MOVIES:
            print 'copied framestarts: '
        if DEBUG_MOVIES:
            print str(self.writesbfmf_framestarts[:i + 1])
        inmovie.h_mov.seek(0)
        pagesize = int(1048576)
        for j in range(firstaddr, lastaddr, pagesize):
            if DEBUG_MOVIES:
                print 'writing page at %d' % inmovie.h_mov.file.tell()
            buf = inmovie.h_mov.read_some_bytes(pagesize)
            self.outfile.write(buf)

        if j < lastaddr:
            if DEBUG_MOVIES:
                print 'writing page at %d' % inmovie.h_mov.file.tell()
            buf = inmovie.h_mov.read_some_bytes(int(lastaddr - pagesize))
            self.outfile.write(buf)
        inmovie.h_mov.close()
        os.remove(tmpfilename)
        return

    def writesbfmf_close(self, frame):
        if hasattr(self, 'outfile') and self.outfile is not None:
            self.writesbfmf_writeindex(frame)
            self.outfile.close()
        return

    def writesbfmf_writeindex(self, frame):
        """
        Writes the index at the end of the file. Index consists of nframes unsigned long longs (Q),
        indicating the positions of each frame
        """
        indexloc = self.outfile.tell()
        nframeswrite = frame - params.start_frame + 1
        if DEBUG_MOVIES:
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
        if bg.bg_type == 'light_on_dark':
            difference_mode = 0
        elif bg.bg_type == 'dark_on_light':
            difference_mode = 1
        else:
            difference_mode = 2
        self.outfile.write(struct.pack('<I', len(__version__)))
        self.outfile.write(__version__)
        self.outfile.write(struct.pack('<2I', int(self.nr), int(self.nc)))
        self.writesbfmf_nframesloc = self.outfile.tell()
        self.outfile.write(struct.pack('<2I', int(self.nframescompress), int(difference_mode)))
        if DEBUG_MOVIES:
            print 'writeheader: nframescompress = ' + str(self.nframescompress)
        stdloc = self.outfile.tell() + struct.calcsize('B') * self.nr * self.nc
        ffloc = stdloc + struct.calcsize('d') * self.nr * self.nc
        self.writesbfmf_indexptrloc = self.outfile.tell()
        self.outfile.write(struct.pack('<Q', 0))
        self.outfile.write(bg.center)
        self.outfile.write(bg.dev)

    def writesbfmf_writeframe(self, isfore, im, stamp, currframe):
        if DEBUG_MOVIES:
            print 'writing frame %d' % currframe
        tmp = isfore.copy()
        tmp.shape = (self.nr * self.nc,)
        i, = num.nonzero(tmp)
        v = im[isfore]
        n = len(i)
        j = currframe - params.start_frame
        self.writesbfmf_framestarts[j] = self.outfile.tell()
        if DEBUG_MOVIES:
            print 'stored in framestarts[%d]' % j
        self.outfile.write(struct.pack('<Id', n, stamp))
        i = i.astype(num.uint32)
        self.outfile.write(i)
        self.outfile.write(v)

    def close(self):
        if hasattr(self, 'h_mov'):
            with self.file_lock:
                try:
                    self.h_mov.close()
                except:
                    print 'Could not close'


class Avi():
    """Read uncompressed AVI movies."""

    def __init__(self, filename):
        self.issbfmf = False
        self.file = open(filename, 'rb')
        self.frame_index = {}
        try:
            self.read_header()
            self.postheader_calculations()
        except Exception as details:
            if DEBUG_MOVIES:
                print 'error reading uncompressed AVI:'
            if DEBUG_MOVIES:
                print details
            raise

        self.filename = filename
        self.chunk_start = self.data_start
        self.timestamp_len = 8
        if hasattr(self, 'newwidth'):
            self.bytes_per_chunk = self.height * self.newwidth + self.timestamp_len
        else:
            self.bytes_per_chunk = self.buf_size + self.timestamp_len
        if DEBUG_MOVIES:
            print 'bits per pix: %d, bytes per chunk %d' % (self.bits_per_pixel, self.bytes_per_chunk)

    def get_all_timestamps(self):
        """Return a Numpy array containing all frames' timestamps."""
        timestamps = num.zeros((self.n_frames,))
        for fr in range(self.n_frames):
            timestamps[fr] = self.make_timestamp(fr)

        return timestamps

    def make_timestamp(self, fr):
        """Approximate timestamp from frame rate recorded in header."""
        if self.frame_delay_us != 0:
            return fr * self.frame_delay_us / 1000000.0
        else:
            if self.time_scale != 0:
                return fr * self.data_rate / float(self.time_scale)
            return fr / 30.0

    def read_header(self):
        RIFF, riff_size, AVI = struct.unpack('4sI4s', self.file.read(12))
        if not RIFF == 'RIFF':
            print 'movie header RIFF error at', RIFF, riff_size, AVI
            raise TypeError('Invalid AVI file. Must be a RIFF file.')
        if not AVI == 'AVI ' and not AVI == 'AVIX':
            print 'movie header AVI error at', RIFF, riff_size, AVI
            raise TypeError("Invalid AVI file. File type must be 'AVI '.")
        LIST, hdrl_size, hdrl = struct.unpack('4sI4s', self.file.read(12))
        hdrlstart = self.file.tell() - 4
        if not LIST == 'LIST':
            print 'movie header LIST 1 error at', LIST, hdrl_size, hdrl
            raise TypeError('Invalid AVI file. Did not find header list.')
        if hdrl == 'hdrl':
            avih, avih_size = struct.unpack('4sI', self.file.read(8))
            if not avih == 'avih':
                print 'movie header avih error at', avih, avih_size
                raise TypeError('Invalid AVI file. Did not find avi header.')
            avihchunkstart = self.file.tell()
            self.frame_delay_us, = struct.unpack('I', self.file.read(4))
            self.file.seek(12, 1)
            self.n_frames, = struct.unpack('I', self.file.read(4))
            self.file.seek(12, 1)
            self.width, self.height = struct.unpack('2I', self.file.read(8))
            if DEBUG_MOVIES:
                print 'width = %d, height = %d' % (self.width, self.height)
            if DEBUG_MOVIES:
                print 'n_frames = %d' % self.n_frames
            self.file.seek(avihchunkstart + avih_size, 0)
            LIST, stream_listsize, strl = struct.unpack('4sI4s', self.file.read(12))
            if not LIST == 'LIST' or not strl == 'strl':
                print 'movie header LIST 2 error at', LIST, strl
                raise TypeError('Invalid AVI file. Did not find stream list.')
            strh, strh_size = struct.unpack('4sI', self.file.read(8))
            if not strh == 'strh':
                print 'movie header strh error at', strh, strh_size
                raise TypeError('Invalid AVI file. Did not find stream header.')
            strhstart = self.file.tell()
            vids, fcc = struct.unpack('4s4s', self.file.read(8))
            if not vids == 'vids':
                print 'movie header vids error at', vids
                raise TypeError('Unsupported AVI file type. First stream found is not a video stream.')
            if fcc not in ['DIB ', '\x00\x00\x00\x00', '', 'RAW ', 'NONE', chr(24) + 'BGR', 'Y8  ']:
                if DEBUG_MOVIES:
                    print 'movie header codec error at', fcc
                raise TypeError('Unsupported AVI file type %s, only uncompressed AVIs supported.' % fcc)
            if DEBUG_MOVIES:
                print 'codec', fcc
            self.file.seek(strhstart + strh_size, 0)
            strf, strf_size = struct.unpack('4sI', self.file.read(8))
            if not strf == 'strf':
                print 'movie header strf error at', strf
                raise TypeError('Invalid AVI file. Did not find strf.')
            strfstart = self.file.tell()
            bitmapheadersize, = struct.unpack('I', self.file.read(4))
            self.file.seek(10, 1)
            self.bits_per_pixel, = struct.unpack('H', self.file.read(2))
            if DEBUG_MOVIES:
                print 'bits_per_pixel = %d' % self.bits_per_pixel
            colormapsize = (strf_size - bitmapheadersize) / 4
            if colormapsize > 0:
                self.isindexed = True
                self.file.seek(strfstart + bitmapheadersize, 0)
                self.colormap = num.frombuffer(self.file.read(4 * colormapsize), num.uint8)
                self.colormap = self.colormap.reshape((colormapsize, 4))
                self.colormap = self.colormap[:, :-1]
                if DEBUG_MOVIES:
                    print 'file is indexed with %d colors' % len(self.colormap)
            else:
                self.isindexed = False
            if self.bits_per_pixel == 24:
                self.isindexed = False
            self.file.seek(hdrlstart + hdrl_size, 0)
        else:
            self.file.seek(-12, os.SEEK_CUR)
        while True:
            LIST, movilist_size = struct.unpack('4sI', self.file.read(8))
            if LIST == 'LIST':
                movi, = struct.unpack('4s', self.file.read(4))
                if DEBUG_MOVIES:
                    print 'looking for movi, found ' + movi
                if movi == 'movi':
                    break
                else:
                    self.file.seek(-4, 1)
            self.file.seek(movilist_size, 1)

        if not movi == 'movi':
            raise TypeError('Invalid AVI file. Did not find movi, found %s.' % movi)
        while True:
            fourcc, chunksize = struct.unpack('4sI', self.file.read(8))
            if DEBUG_MOVIES:
                print 'read fourcc=%s, chunksize=%d' % (fourcc, chunksize)
            if fourcc == '00db' or fourcc == '00dc':
                self.file.seek(-8, 1)
                break
            self.file.seek(chunksize, 1)

        self.buf_size = chunksize
        if DEBUG_MOVIES:
            print 'chunk size: ', self.buf_size
        approx_file_len = self.buf_size * self.n_frames
        cur_pos = self.file.tell()
        self.file.seek(0, os.SEEK_END)
        real_file_len = self.file.tell()
        self.file.seek(cur_pos)
        if real_file_len > approx_file_len * 1.1:
            print 'approximate file length %ld bytes, real length %ld' % (approx_file_len, real_file_len)
            self._header_n_frames = self.n_frames
            self.n_frames = int(num.floor((real_file_len - cur_pos) / self.buf_size))
            print 'guessing %d frames in movie, although header said %d' % (self.n_frames, self._header_n_frames)

    def postheader_calculations(self):
        """Tidy up some initialization, immediately after reading header."""
        self.data_start = self.file.tell()
        depth = self.bits_per_pixel / 8
        unpaddedframesize = self.width * self.height * depth
        if unpaddedframesize == self.buf_size:
            self.padwidth = 0
            self.padheight = 0
        else:
            if unpaddedframesize + self.width * depth == self.buf_size:
                self.padwidth = 0
                self.padheight = 1
            elif unpaddedframesize + self.height * depth == self.buf_size:
                self.padwidth = 1
                self.padheight = 0
            else:
                raise TypeError('Invalid AVI file. Frame size (%d) does not match width * height * bytesperpixel (%d*%d*%d).' % (self.buf_size, self.width, self.height, depth))
            if self.bits_per_pixel == 24:
                self.format = 'RGB'
            elif self.isindexed:
                self.format = 'INDEXED'
            elif self.bits_per_pixel == 8:
                self.format = 'MONO8'
            else:
                raise TypeError('Unsupported AVI type. bitsperpixel must be 8 or 24, not %d.' % self.bits_per_pixel)
            if DEBUG_MOVIES:
                print 'format = ' + str(self.format)
            if self.n_frames == 0:
                loccurr = self.file.tell()
                self.file.seek(0, 2)
                locend = self.file.tell()
                self.n_frames = int(num.floor((locend - self.data_start) / (self.buf_size + 8)))
                print 'n frames = 0; setting to %d' % self.n_frames
            currentNframes = self.n_frames
            while True:
                frameNumber = self.n_frames - 1
                try:
                    self.get_frame(frameNumber)
                except:
                    pass

                if self.n_frames == currentNframes:
                    break
                currentNframes = self.n_frames

    def nearest_indexed_frame(self, framenumber):
        """Return nearest known frame index less than framenumber."""
        keys = self.frame_index.keys()
        keys.sort()
        nearest = None
        for key in keys:
            if framenumber > key:
                nearest = key
            else:
                break

        return nearest

    def build_index(self, to_fr):
        """Build index successively up to a selected frame."""
        near_idx = self.nearest_indexed_frame(to_fr)
        if near_idx is None:
            self.file.seek(self.data_start, os.SEEK_SET)
            self.framenumber = 0
            try:
                frame, stamp = self.get_next_frame()
            except:
                if params.interactive:
                    pb.Destroy()
                raise
            else:
                from_fr = 0

        else:
            from_fr = near_idx
        if params.interactive and to_fr - from_fr > 10:
            show_pb = True
        else:
            show_pb = False
        if show_pb:
            pb = wx.ProgressDialog('Building Frame Index', 'Calculating file location for frame %d' % to_fr, to_fr - from_fr, None, wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT | wx.PD_REMAINING_TIME)
        max_increment = 100
        increment = max_increment
        last_fr = from_fr
        this_fr = min(from_fr + increment, to_fr)
        failed_fr = last_fr
        while True:
            self.file.seek((self.buf_size + 8) * (this_fr - last_fr) + self.frame_index[last_fr], os.SEEK_SET)
            self.framenumber = this_fr
            try:
                frame, stamp = self.get_next_frame()
                if this_fr >= to_fr:
                    break
            except:
                if increment == 1:
                    if show_pb:
                        pb.Destroy()
                    raise
                else:
                    increment = max(int(increment / 10), 1)
                    failed_fr = last_fr
                    this_fr = min(last_fr + increment, to_fr)
            else:
                if increment != max_increment and this_fr - failed_fr >= 10 * increment:
                    increment = min(10 * increment, max_increment)
                last_fr = this_fr
                this_fr = min(last_fr + increment, to_fr)

            if show_pb:
                keepgoing, skip = pb.Update(this_fr - from_fr)
                if not keepgoing:
                    pb.Destroy()
                    raise IndexError("didn't finish building index to %d" % to_fr)

        if show_pb:
            pb.Destroy()
        return

    def get_frame(self, framenumber):
        """Read frame from file and return as NumPy array."""
        if DEBUG_MOVIES:
            print 'uncompressed get_frame(%d)' % framenumber
        if framenumber < 0:
            raise IndexError
        if framenumber >= self.n_frames:
            raise NoMoreFramesException
        self.framenumber = framenumber
        if framenumber in self.frame_index:
            if DEBUG_MOVIES:
                print 'calling frame %d from index at %d' % (framenumber, self.frame_index[framenumber])
            self.file.seek(self.frame_index[framenumber], os.SEEK_SET)
            return self.get_next_frame()
        else:
            near_idx = self.nearest_indexed_frame(framenumber)
            if near_idx is not None:
                offset = framenumber - near_idx
                self.file.seek((self.buf_size + 8) * offset + self.frame_index[near_idx], os.SEEK_SET)
            else:
                self.file.seek(self.data_start + (self.buf_size + 8) * framenumber)
            try:
                return self.get_next_frame()
            except ValueError:
                if framenumber == 0:
                    raise
                self.build_index(framenumber)
                self.file.seek(self.frame_index[framenumber], os.SEEK_SET)
                return self.get_next_frame()

            return

    def get_next_frame(self):
        """returns next frame"""
        file_data = self.file.read(8)
        if len(file_data) != 8:
            cur_pos = self.file.tell()
            self.file.seek(0, os.SEEK_END)
            if self.file.tell() >= cur_pos:
                raise IndexError('error seeking frame %d -- file not readable' % self.framenumber)
            else:
                self.n_frames = self.framenumber - 1
                self.framenumber = self.n_frames
                return self.get_next_frame()
        this_frame_id, frame_size = struct.unpack('4sI', file_data)
        if DEBUG_MOVIES:
            print 'frame id=%s, sz=%d' % (this_frame_id, frame_size)
        if this_frame_id == 'idx1' or this_frame_id == 'ix00' or this_frame_id == 'ix01':
            a = self.file.read(frame_size)
            this_frame_id, frame_size = struct.unpack('4sI', self.file.read(8))
            if DEBUG_MOVIES:
                print 'skipped index; frame id=' + str(this_frame_id) + ', sz=' + str(frame_size)
        if this_frame_id == 'RIFF':
            self.file.seek(-8, os.SEEK_CUR)
            self.read_header()
            this_frame_id, frame_size = struct.unpack('4sI', self.file.read(8))
            if DEBUG_MOVIES:
                print 'skipped another header; frame id=' + str(this_frame_id) + ', sz=' + str(frame_size)
        if hasattr(self, 'frame_id') and this_frame_id != self.frame_id:
            tries = 0
            while this_frame_id != self.frame_id and tries < 64:
                self.file.seek(-7, os.SEEK_CUR)
                this_frame_id, frame_size = struct.unpack('4sI', self.file.read(8))
                tries += 1

            if DEBUG_MOVIES:
                print 'skipped forward %d bytes; now id=%s, sz=%d' % (tries, this_frame_id, frame_size)
        if frame_size != self.buf_size:
            if hasattr(self, '_header_n_frames') and (self.framenumber == self._header_n_frames or self.framenumber == self._header_n_frames - 1):
                self.n_frames = self.framenumber
                print 'resetting frame count to', self.n_frames
                raise IndexError('Error reading frame %d; header said only %d frames were present' % (self.framenumber, self._header_n_frames))
            else:
                raise ValueError('Frame size %d on disk does not equal uncompressed size %d; movie must be uncompressed' % (frame_size, self.buf_size))
        if not hasattr(self, 'frame_id'):
            self.frame_id = this_frame_id
        elif this_frame_id != self.frame_id:
            if DEBUG_MOVIES:
                print 'looking for header %s; found %s' % (self.frame_id, this_frame_id)
            raise ValueError('error seeking frame start: unknown data header')
        frame_data = self.file.read(frame_size)
        frame = num.fromstring(frame_data, num.uint8)
        width = self.width + self.padwidth
        height = self.height + self.padheight
        if self.isindexed:
            frame = self.colormap[frame, :]
            if params.movie_index_transpose:
                frame.resize((width, height, 3))
                frame = frame[:self.width, :self.height, :]
            else:
                frame.resize((height, width, 3))
                frame = frame[:self.height, :self.width, :]
            tmp = frame.astype(float)
            tmp = tmp[:, :, 0] * 0.3 + tmp[:, :, 1] * 0.59 + tmp[:, :, 2] * 0.11
            if params.movie_index_transpose:
                tmp = tmp.T
            frame = tmp.astype(num.uint8)
        elif frame.size == width * height:
            frame.resize((height, width))
            frame = frame[:self.height, :self.width]
        elif frame.size == width * height * 3:
            frame.resize((height, width * 3))
            tmp = frame.astype(float)
            tmp = tmp[:, 2:width * 3:3] * 0.3 + tmp[:, 1:width * 3:3] * 0.59 + tmp[:, 0:width * 3:3] * 0.11
            tmp = tmp[:self.height, :self.width]
            frame = tmp.astype(num.uint8)
        elif frame.size % height == 0:
            self.newwidth = frame.size / height
            if abs(self.newwidth - width) < 10:
                frame.resize((self.newwidth, height))
                frame = frame[:self.width, :self.height]
            else:
                raise ValueError('apparent new width = %d; expected width = %d' % (
                 height, self.newwidth))
        else:
            print self.width, self.height, self.padwidth, self.padheight
            print self.width * self.height, frame_size, frame.size, self.width * self.height * 3, frame_size / 3
            print frame_size / self.width / 3, frame_size / self.height / 3, frame_size % width, frame_size % height
            raise ValueError('apparent new width is not integral; mod = %d' % (frame.size % height))
        if self.framenumber not in self.frame_index:
            self.frame_index[self.framenumber] = self.file.tell() - frame_size - 8
            if DEBUG_MOVIES:
                print 'added frame %d to index at %d' % (self.framenumber, self.frame_index[self.framenumber])
        return (
         frame, self.make_timestamp(self.framenumber))

    def get_n_frames(self):
        return self.n_frames

    def get_width(self):
        if hasattr(self, 'newwidth'):
            return self.newwidth
        else:
            return self.width

    def get_height(self):
        return self.height

    def seek(self, framenumber):
        if framenumber < 0:
            framenumber = self.n_frames + framenumber
        if framenumber in self.frame_index:
            seek_to = self.frame_index[framenumber]
        else:
            seek_to = self.chunk_start + self.bytes_per_chunk * framenumber
        self.file.seek(seek_to)


class CompressedAvi():
    """Use OpenCV to read compressed avi files."""

    def __init__(self, filename):
        if DEBUG_MOVIES:
            print 'Trying to read compressed AVI'
        self.issbfmf = False
        self.source = cv2.VideoCapture(filename)
        if not self.source.isOpened():
            raise IOError('OpenCV could not open the movie %s' % filename)
        self.start_time = self.source.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        self.fps = self.source.get(cv2.cv.CV_CAP_PROP_FPS)
        self.n_frames = int(self.source.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        self.frame_delay_us = 1000000.0 / self.fps
        self.filename = filename
        self.width = int(self.source.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.height = int(self.source.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        self.MAXBUFFERSIZE = num.round(200000000.0 / self.width / self.height)
        self.keyframe_period = 100
        self.buffersize = min(self.MAXBUFFERSIZE, self.keyframe_period)
        if DEBUG_MOVIES:
            print 'buffersize set to ' + str(self.buffersize)
        retval, im = self.source.read()
        im = num.fromstring(im.data, num.uint8)
        self.color_depth = len(im) / self.width / self.height
        if self.color_depth != 1 and self.color_depth != 3:
            raise ValueError('color_depth = %d, only know how to deal with color_depth = 1 or colr_depth = 3' % self.color_depth)
        self.bits_per_pixel = self.color_depth * 8
        self.buffer = num.zeros((self.height, self.width, self.buffersize), dtype=num.uint8)
        self.bufferts = num.zeros(self.buffersize)
        self.seek(0)
        frame, ts = self.get_next_frame_and_reset_buffer()
        if DEBUG_MOVIES:
            print 'Done initializing CompressedAVI'

    def get_all_timestamps(self):
        return num.arange(self.n_frames) / self.fps + self.start_time

    def get_frame(self, framenumber):
        """Read frame from file and return as NumPy array."""
        if framenumber < 0:
            raise IndexError
        if framenumber >= self.bufferframe0 and framenumber < self.bufferframe1:
            off = num.mod(framenumber - self.bufferframe0 + self.bufferoff0, self.buffersize)
            if DEBUG_MOVIES:
                print 'frame %d is in buffer at offset %d' % (framenumber, off)
            return (
             self.buffer[:, :, off].copy(), self.bufferts[off])
        if framenumber == self.currframe:
            if DEBUG_MOVIES:
                print 'frame %d is the next frame, just calling get_next_frame' % framenumber
            return self.get_next_frame()
        self.seek(framenumber)
        return self.get_next_frame_and_reset_buffer()

    def get_next_frame_and_reset_buffer(self):
        self.bufferframe0 = self.currframe
        self.bufferframe1 = self.currframe + 1
        self.bufferoff0 = 0
        frame, ts = self._get_next_frame_helper()
        self.buffer[:, :, 0] = frame.copy()
        self.bufferts[0] = ts
        if self.buffersize > 1:
            self.bufferoff = 1
        else:
            self.bufferoff = 0
        self.currframe += 1
        self.prevts = ts
        return (
         frame, ts)

    def _get_next_frame_helper(self):
        ts = self.source.get(cv2.cv.CV_CAP_PROP_POS_MSEC) / 1000.0
        retval, im = self.source.read()
        if not retval:
            raise IOError('OpenCV failed reading frame %d' % self.currframe)
        frame = num.fromstring(im.data, num.uint8)
        if self.color_depth == 1:
            frame.resize((im.height, im.width))
        else:
            frame.resize((self.height, self.width * 3))
            tmp = frame.astype(float)
            tmp = tmp[:, 2:self.width * 3:3] * 0.3 + tmp[:, 1:self.width * 3:3] * 0.59 + tmp[:, 0:self.width * 3:3] * 0.11
            frame = tmp.astype(num.uint8)
        frame = num.flipud(frame)
        return (
         frame, ts)

    def get_next_frame(self):
        frame, ts = self._get_next_frame_helper()
        self.bufferframe1 += 1
        if self.bufferoff0 == self.bufferoff:
            self.bufferframe0 += 1
            if self.buffersize > 1:
                self.bufferoff0 += 1
            if DEBUG_MOVIES:
                print 'erasing first frame, bufferframe0 is now %d, bufferoff0 is now %d' % (self.bufferframe0, self.bufferoff0)
        if DEBUG_MOVIES:
            print 'buffer frames: [%d,%d), bufferoffset0 = %d' % (self.bufferframe0, self.bufferframe1, self.bufferoff0)
        self.buffer[:, :, self.bufferoff] = frame.copy()
        self.bufferts[self.bufferoff] = ts
        if DEBUG_MOVIES:
            print 'read into buffer[%d], ts = %f' % (self.bufferoff, ts)
        self.bufferoff += 1
        if self.bufferoff >= self.buffersize:
            self.bufferoff = 0
        if DEBUG_MOVIES:
            print 'incremented bufferoff to %d' % self.bufferoff
        self.currframe += 1
        self.prevts = ts
        if DEBUG_MOVIES:
            print 'updated currframe to %d, prevts to %f' % (self.currframe, self.prevts)
        return (
         frame, ts)

    def _estimate_fps(self):
        if DEBUG_MOVIES:
            print 'Estimating fps'
        self.source._seek(self.ZERO)
        if DEBUG_MOVIES:
            print 'First seek succeeded'
        ts0 = self.source.get_next_video_timestamp()
        ts1 = ts0
        if DEBUG_MOVIES:
            print 'initial time stamp = ' + str(ts0)
        nsamples = 200
        if DEBUG_MOVIES:
            print 'nsamples = ' + str(nsamples)
        i = 0
        while True:
            im = self.source.get_next_video_frame()
            ts = self.source.get_next_video_timestamp()
            if DEBUG_MOVIES:
                print 'i = %d, ts = ' % i + str(ts)
            if ts is None or num.isnan(ts) or ts <= ts1:
                break
            i = i + 1
            ts1 = ts
            if i >= nsamples:
                break

        if ts1 <= ts0:
            raise ValueError('Could not compute the fps in the compressed movie')
        self.fps = float(i) / (ts1 - ts0)
        if DEBUG_MOVIES:
            print 'Estimated frames-per-second = %f' % self.fps
        return

    def _estimate_keyframe_period(self):
        if DEBUG_MOVIES:
            print 'Estimating keyframe period'
        self.source._seek(self.ZERO)
        ts0 = self.source.get_next_video_timestamp()
        if DEBUG_MOVIES:
            print 'After first seek, ts0 intialized to ' + str(ts0)
        i = 1
        foundfirst = False
        while True:
            self.source._seek(float(i) / self.fps)
            ts = self.source.get_next_video_timestamp()
            if ts is None or num.isnan(ts):
                if foundfirst:
                    self.keyframe_period = i
                    self.keyframe_period_s = self.keyframe_period / self.fps
                else:
                    self.keyframe_period = self.n_frames + 1
                    self.keyframe_period_s = self.duration_seconds + self.fps
                    if DEBUG_MOVIES:
                        'Only keyframe found at start of movie, setting keyframe_period = n_frames + 1 = %d, keyframe_period_s = duration_seconds + fps = %f' % (self.keyframe_period, self.keyframe_period_s)
                return
            if ts > ts0:
                if foundfirst:
                    break
                else:
                    foundfirst = True
                    i0 = i
                    ts0 = ts
            i = i + 1

        if DEBUG_MOVIES:
            print 'i = %d, i0 = %d' % (i, i0)
        self.keyframe_period = i - i0
        self.keyframe_period_s = self.keyframe_period / self.fps
        if DEBUG_MOVIES:
            print 'Estimated keyframe period = ' + str(self.keyframe_period)
        return

    def get_n_frames(self):
        return self.n_frames

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def seek(self, framenumber):
        self.currframe = framenumber
        self.source.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.currframe)
        return self.currframe


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
        if params.interactive:
            wx.Yield()
        if params.app_instance is not None and not params.app_instance.alive:
            offsets = offsets[:i - f0 + 1]
            break

    offsets -= movilistloc + 4
    write_avi_index(movie, offsets, outstream)
    outstream.close()
    return


def write_avi_index(movie, offsets, outstream):
    idx1size = 8 + 16 * len(offsets)
    BYTESPERPIXEL = 3
    bytesperframe = int(movie.get_width() * movie.get_height() * BYTESPERPIXEL)
    write_chunk_header('idx1', int(idx1size), outstream)
    for o in offsets:
        try:
            bin_offset = struct.pack('I', int(o))
        except struct.error:
            traceback.print_exc()
            print 'writing index %d' % o
            break

        outstream.write(struct.pack('4s', '00db'))
        outstream.write(struct.pack('I', 16))
        outstream.write(bin_offset)
        outstream.write(struct.pack('I', int(bytesperframe)))


def write_avi_frame(movie, tracks, i, outstream):
    height = movie.get_height()
    width = movie.get_width()
    BYTESPERPIXEL = 3
    bytesperframe = width * height * BYTESPERPIXEL
    if tracks is None:
        return
    else:
        if i >= len(tracks):
            return
        j = params.start_frame + i
        try:
            frame, last_timestamp = movie.get_frame(j)
        except (IndexError, NoMoreFramesException):
            return

        ellipses = tracks[i]
        old_pts = []
        early_frame = int(max(0, i - params.tail_length))
        for j in range(early_frame, i + 1):
            dataframe = tracks[j]
            these_pts = []
            ellplot = []
            for ellipse in dataframe.itervalues():
                if num.isnan(ellipse.center.x) or num.isnan(ellipse.center.y):
                    continue
                these_pts.append((ellipse.center.x, ellipse.center.y,
                 ellipse.identity))
                ellplot.append(ellipse)

            old_pts.append(these_pts)

        bitmap, resize, img_size = annotate_bmp(frame, ellplot, old_pts, params.ellipse_thickness, [
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
    elif hasattr(movie.h_mov, 'frame_delay_us'):
        microsecperframe = movie.h_mov.frame_delay_us
    else:
        microsecperframe = estimate_frame_delay_us(movie.h_mov)
    outstream.write(struct.pack('I', int(round(microsecperframe))))
    framespersec = int(round(1000000.0 / microsecperframe))
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
    outstream.write(struct.pack('4s', 'DIB '))
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
    try:
        outstream.write(struct.pack('4sI', chunktype, chunksize))
    except struct.error as details:
        traceback.print_exc()
        print "writing '%s' with size %d" % (chunktype, chunksize)
        outstream.write(struct.pack('4sI', chunktype, 0))


def write_list_header(listtype, listsize, outstream):
    try:
        outstream.write(struct.pack('4sI4s', 'LIST', listsize, listtype))
    except struct.error as details:
        traceback.print_exc()
        print "writing '%s' with size %d" % (listtype, listsize)
        outstream.write(struct.pack('4sI4s', 'LIST', 0, listtype))


def estimate_frame_delay_us(mov):
    if not hasattr(mov, 'chunk_start'):
        return 0
    else:
        if mov.issbfmf:
            return 50000.0
        mov.file.seek(mov.chunk_start)
        stamp0 = mov.get_next_timestamp()
        mov.file.seek(mov.chunk_start + mov.bytes_per_chunk * (mov.n_frames - 1))
        stamp1 = mov.get_next_timestamp()
        frame_delay_us = float(stamp1 - stamp0) / float(mov.n_frames - 1) * 1000000.0
        return frame_delay_us