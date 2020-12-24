# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/newavi.py
# Compiled at: 2008-08-06 20:33:57


class Avi:
    """Read uncompressed AVI movies."""

    def __init__(self, filename, fmfmode=False):
        self.fmfmode = fmfmode
        self.file = open(filename, 'rb')
        self.read_header()
        self.filename = filename
        self.chunk_start = self.data_start
        self.timestamp_len = 8
        if hasattr(self, 'newwidth'):
            self.bytes_per_chunk = self.height * self.newwidth + self.timestamp_len
        else:
            self.bytes_per_chunk = self.buf_size + self.timestamp_len
        self.bits_per_pixel = 8

    def read_header(self):
        (file_type, riff_size) = struct.unpack('4sI', self.file.read(8))
        assert file_type == 'RIFF'
        stream_type = self.file.read(4)
        assert stream_type == 'AVI '
        (header_list, header_listsize, header_listtype) = struct.unpack('4sI4s', self.file.read(12))
        assert header_list == 'LIST' and header_listtype == 'hdrl'
        (avi_str, avi_note) = struct.unpack('4sI', self.file.read(8))
        assert avi_str == 'avih'
        avi_header = self.file.read(56)
        (self.frame_delay_us, AVI_data_rate, padding_size, AVI_flags, self.n_frames, n_preview_streams, n_data_streams, avi_buf_size, self.width, self.height, self.time_scale, self.data_rate, self.start_time, self.AVI_chunk_size) = struct.unpack('14I', avi_header)
        if n_data_streams != 1:
            raise TypeError('file must contain only one data stream')
        if avi_buf_size != 0:
            self.buf_size = avi_buf_size
        (stream_list, stream_listsize, stream_listtype) = struct.unpack('4sI4s', self.file.read(12))
        assert stream_list == 'LIST' and stream_listtype == 'strl'
        (stream_str, stream_note) = struct.unpack('4sI', self.file.read(8))
        assert stream_str == 'strh'
        stream_header = self.file.read(56)
        (fccType, fccHandler, stream_flags, priority, frames_interleave, stream_scale, stream_rate, stream_start, stream_length, stream_buf_size, stream_quality, stream_sample_size, x, y, w, h) = struct.unpack('4s4s10I4H', stream_header)
        if fccType != 'vids':
            raise TypeError('stream type must be video')
        if fccHandler not in ('DIB ', '\x00\x00\x00\x00', ''):
            raise ValueError('video must be uncompressed; found fccHandler %s' % fccHandler)
        if stream_buf_size != 0:
            if hasattr(self, 'buf_size'):
                assert self.buf_size == stream_buf_size
            else:
                self.buf_size = stream_buf_size
        (bmp_str, bmp_note) = struct.unpack('4sI', self.file.read(8))
        assert bmp_str == 'strf'
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
            raise ValueError('movie must be uncompressed')
        if not hasattr(self, 'frame_id'):
            self.frame_id = this_frame_id
        elif this_frame_id != self.frame_id:
            raise ValueError('error seeking frame start: unknown data header')
        frame_data = self.file.read(frame_size)
        frame = num.fromstring(frame_data, num.uint8)
        if frame.size == self.width * self.height:
            frame.resize((self.height, self.width))
        elif frame.size == self.width * self.height * 3:
            raise TypeError('movie must be grayscale')
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