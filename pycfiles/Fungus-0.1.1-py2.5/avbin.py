# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/media/avbin.py
# Compiled at: 2009-02-07 06:48:50
"""Use avbin to decode audio and video media.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: avbin.py 2084 2008-05-27 12:42:19Z Alex.Holkner $'
from pyglet.media import MediaFormatException, StreamingSource, VideoFormat, AudioFormat, AudioData
import pyglet
from pyglet import gl
from pyglet.gl import gl_info
from pyglet import image
import pyglet.lib, ctypes
av = pyglet.lib.load_library('avbin', darwin='/usr/local/lib/libavbin.dylib')
AVBIN_RESULT_ERROR = -1
AVBIN_RESULT_OK = 0
AVbinResult = ctypes.c_int
AVBIN_STREAM_TYPE_UNKNOWN = 0
AVBIN_STREAM_TYPE_VIDEO = 1
AVBIN_STREAM_TYPE_AUDIO = 2
AVbinStreamType = ctypes.c_int
AVBIN_SAMPLE_FORMAT_U8 = 0
AVBIN_SAMPLE_FORMAT_S16 = 1
AVBIN_SAMPLE_FORMAT_S24 = 2
AVBIN_SAMPLE_FORMAT_S32 = 3
AVBIN_SAMPLE_FORMAT_FLOAT = 4
AVbinSampleFormat = ctypes.c_int
AVBIN_LOG_QUIET = -8
AVBIN_LOG_PANIC = 0
AVBIN_LOG_FATAL = 8
AVBIN_LOG_ERROR = 16
AVBIN_LOG_WARNING = 24
AVBIN_LOG_INFO = 32
AVBIN_LOG_VERBOSE = 40
AVBIN_LOG_DEBUG = 48
AVbinLogLevel = ctypes.c_int
AVbinFileP = ctypes.c_void_p
AVbinStreamP = ctypes.c_void_p
Timestamp = ctypes.c_int64

class AVbinFileInfo(ctypes.Structure):
    _fields_ = [
     (
      'structure_size', ctypes.c_size_t),
     (
      'n_streams', ctypes.c_int),
     (
      'start_time', Timestamp),
     (
      'duration', Timestamp),
     (
      'title', ctypes.c_char * 512),
     (
      'author', ctypes.c_char * 512),
     (
      'copyright', ctypes.c_char * 512),
     (
      'comment', ctypes.c_char * 512),
     (
      'album', ctypes.c_char * 512),
     (
      'year', ctypes.c_int),
     (
      'track', ctypes.c_int),
     (
      'genre', ctypes.c_char * 32)]


class _AVbinStreamInfoVideo(ctypes.Structure):
    _fields_ = [
     (
      'width', ctypes.c_uint),
     (
      'height', ctypes.c_uint),
     (
      'sample_aspect_num', ctypes.c_int),
     (
      'sample_aspect_den', ctypes.c_int)]


class _AVbinStreamInfoAudio(ctypes.Structure):
    _fields_ = [
     (
      'sample_format', ctypes.c_int),
     (
      'sample_rate', ctypes.c_uint),
     (
      'sample_bits', ctypes.c_uint),
     (
      'channels', ctypes.c_uint)]


class _AVbinStreamInfoUnion(ctypes.Union):
    _fields_ = [
     (
      'video', _AVbinStreamInfoVideo),
     (
      'audio', _AVbinStreamInfoAudio)]


class AVbinStreamInfo(ctypes.Structure):
    _fields_ = [
     (
      'structure_size', ctypes.c_size_t),
     (
      'type', ctypes.c_int),
     (
      'u', _AVbinStreamInfoUnion)]


class AVbinPacket(ctypes.Structure):
    _fields_ = [
     (
      'structure_size', ctypes.c_size_t),
     (
      'timestamp', Timestamp),
     (
      'stream_index', ctypes.c_int),
     (
      'data', ctypes.POINTER(ctypes.c_uint8)),
     (
      'size', ctypes.c_size_t)]


AVbinLogCallback = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
av.avbin_get_version.restype = ctypes.c_int
av.avbin_get_ffmpeg_revision.restype = ctypes.c_int
av.avbin_get_audio_buffer_size.restype = ctypes.c_size_t
av.avbin_have_feature.restype = ctypes.c_int
av.avbin_have_feature.argtypes = [ctypes.c_char_p]
av.avbin_init.restype = AVbinResult
av.avbin_set_log_level.restype = AVbinResult
av.avbin_set_log_level.argtypes = [AVbinLogLevel]
av.avbin_set_log_callback.argtypes = [AVbinLogCallback]
av.avbin_open_filename.restype = AVbinFileP
av.avbin_open_filename.argtypes = [ctypes.c_char_p]
av.avbin_close_file.argtypes = [AVbinFileP]
av.avbin_seek_file.argtypes = [AVbinFileP, Timestamp]
av.avbin_file_info.argtypes = [AVbinFileP, ctypes.POINTER(AVbinFileInfo)]
av.avbin_stream_info.argtypes = [AVbinFileP, ctypes.c_int,
 ctypes.POINTER(AVbinStreamInfo)]
av.avbin_open_stream.restype = ctypes.c_void_p
av.avbin_open_stream.argtypes = [AVbinFileP, ctypes.c_int]
av.avbin_close_stream.argtypes = [AVbinStreamP]
av.avbin_read.argtypes = [
 AVbinFileP, ctypes.POINTER(AVbinPacket)]
av.avbin_read.restype = AVbinResult
av.avbin_decode_audio.restype = ctypes.c_int
av.avbin_decode_audio.argtypes = [AVbinStreamP,
 ctypes.c_void_p, ctypes.c_size_t,
 ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
av.avbin_decode_video.restype = ctypes.c_int
av.avbin_decode_video.argtypes = [AVbinStreamP,
 ctypes.c_void_p, ctypes.c_size_t,
 ctypes.c_void_p]

def get_version():
    return av.avbin_get_version()


class AVbinException(MediaFormatException):
    pass


def timestamp_from_avbin(timestamp):
    return float(timestamp) / 1000000


def timestamp_to_avbin(timestamp):
    return int(timestamp * 1000000)


class BufferedPacket(object):

    def __init__(self, packet):
        self.timestamp = packet.timestamp
        self.stream_index = packet.stream_index
        self.data = (ctypes.c_uint8 * packet.size)()
        self.size = packet.size
        ctypes.memmove(self.data, packet.data, self.size)


class BufferedImage(object):

    def __init__(self, image, timestamp):
        self.image = image
        self.timestamp = timestamp


class AVbinSource(StreamingSource):

    def __init__(self, filename, file=None):
        if file is not None:
            raise NotImplementedError('TODO: Load from file stream')
        self._file = av.avbin_open_filename(filename)
        if not self._file:
            raise AVbinException('Could not open "%s"' % filename)
        self._video_stream = None
        self._audio_stream = None
        file_info = AVbinFileInfo()
        file_info.structure_size = ctypes.sizeof(file_info)
        av.avbin_file_info(self._file, ctypes.byref(file_info))
        self._duration = timestamp_from_avbin(file_info.duration)
        for i in range(file_info.n_streams):
            info = AVbinStreamInfo()
            info.structure_size = ctypes.sizeof(info)
            av.avbin_stream_info(self._file, i, info)
            if info.type == AVBIN_STREAM_TYPE_VIDEO and not self._video_stream:
                stream = av.avbin_open_stream(self._file, i)
                if not stream:
                    continue
                self.video_format = VideoFormat(width=info.u.video.width, height=info.u.video.height)
                if info.u.video.sample_aspect_num != 0:
                    self.video_format.sample_aspect = float(info.u.video.sample_aspect_num) / info.u.video.sample_aspect_den
                self._video_stream = stream
                self._video_stream_index = i
            elif info.type == AVBIN_STREAM_TYPE_AUDIO and info.u.audio.sample_bits in (8,
                                                                                       16) and info.u.audio.channels in (1,
                                                                                                                         2) and not self._audio_stream:
                stream = av.avbin_open_stream(self._file, i)
                if not stream:
                    continue
                self.audio_format = AudioFormat(channels=info.u.audio.channels, sample_size=info.u.audio.sample_bits, sample_rate=info.u.audio.sample_rate)
                self._audio_stream = stream
                self._audio_stream_index = i

        self._packet = AVbinPacket()
        self._packet.structure_size = ctypes.sizeof(self._packet)
        self._packet.stream_index = -1
        self._buffered_packets = []
        self._buffer_streams = []
        self._buffered_images = []
        if self.audio_format:
            self._audio_packet_ptr = 0
            self._audio_packet_size = 0
            self._audio_packet_timestamp = 0
            self._audio_buffer = (ctypes.c_uint8 * av.avbin_get_audio_buffer_size())()
            self._buffer_streams.append(self._audio_stream_index)
        if self.video_format:
            self._buffer_streams.append(self._video_stream_index)
            self._force_next_video_image = True
            self._last_video_timestamp = None
        return

    def __del__(self):
        try:
            if self._video_stream:
                av.avbin_close_stream(self._video_stream)
            if self._audio_stream:
                av.avbin_close_stream(self._audio_stream)
            av.avbin_close_file(self._file)
        except:
            pass

    def _seek(self, timestamp):
        av.avbin_seek_file(self._file, timestamp_to_avbin(timestamp))
        self._buffered_packets = []
        self._buffered_images = []
        self._audio_packet_size = 0
        self._force_next_video_image = True
        self._last_video_timestamp = None
        return

    def _get_packet_for_stream(self, stream_index):
        for packet in self._buffered_packets:
            if packet.stream_index == stream_index:
                self._buffered_packets.remove(packet)
                return packet

        while True:
            if av.avbin_read(self._file, self._packet) != AVBIN_RESULT_OK:
                return
            elif self._packet.stream_index == stream_index:
                return self._packet
            elif self._packet.stream_index == self._video_stream_index:
                buffered_image = self._decode_video_packet(self._packet)
                if buffered_image:
                    self._buffered_images.append(buffered_image)
            elif self._packet.stream_index in self._buffer_streams:
                self._buffered_packets.append(BufferedPacket(self._packet))

        return

    def _get_audio_data(self, bytes):
        while True:
            while self._audio_packet_size > 0:
                size_out = ctypes.c_int(len(self._audio_buffer))
                used = av.avbin_decode_audio(self._audio_stream, self._audio_packet_ptr, self._audio_packet_size, self._audio_buffer, size_out)
                if used < 0:
                    self._audio_packet_size = 0
                    break
                self._audio_packet_ptr.value += used
                self._audio_packet_size -= used
                if size_out.value <= 0:
                    continue
                buffer = ctypes.string_at(self._audio_buffer, size_out)
                duration = float(len(buffer)) / self.audio_format.bytes_per_second
                timestamp = self._audio_packet_timestamp
                self._audio_packet_timestamp += duration
                return AudioData(buffer, len(buffer), timestamp, duration)

            packet = self._get_packet_for_stream(self._audio_stream_index)
            if not packet:
                return
            self._audio_packet_timestamp = timestamp_from_avbin(packet.timestamp)
            self._audio_packet = packet
            self._audio_packet_ptr = ctypes.cast(packet.data, ctypes.c_void_p)
            self._audio_packet_size = packet.size

        return

    def _init_texture(self, player):
        if not self.video_format:
            return
        width = self.video_format.width
        height = self.video_format.height
        if gl_info.have_extension('GL_ARB_texture_rectangle'):
            texture = image.Texture.create_for_size(gl.GL_TEXTURE_RECTANGLE_ARB, width, height, internalformat=gl.GL_RGB)
        else:
            texture = image.Texture.create_for_size(gl.GL_TEXTURE_2D, width, height, internalformat=gl.GL_RGB)
            if texture.width != width or texture.height != height:
                texture = texture.get_region(0, 0, width, height)
        player._texture = texture
        t = list(player._texture.tex_coords)
        player._texture.tex_coords = t[9:12] + t[6:9] + t[3:6] + t[:3]

    def _decode_video_packet(self, packet):
        timestamp = timestamp_from_avbin(packet.timestamp)
        width = self.video_format.width
        height = self.video_format.height
        pitch = width * 3
        buffer = (ctypes.c_uint8 * (pitch * height))()
        result = av.avbin_decode_video(self._video_stream, packet.data, packet.size, buffer)
        if result < 0:
            return
        return BufferedImage(image.ImageData(width, height, 'RGB', buffer, pitch), timestamp)

    def _next_image(self):
        img = None
        while not img:
            packet = self._get_packet_for_stream(self._video_stream_index)
            if not packet:
                return
            img = self._decode_video_packet(packet)

        return img

    def get_next_video_timestamp(self):
        if not self.video_format:
            return
        try:
            img = self._buffered_images[0]
        except IndexError:
            img = self._next_image()
            self._buffered_images.append(img)

        if img:
            return img.timestamp

    def get_next_video_frame(self):
        if not self.video_format:
            return
        try:
            img = self._buffered_images.pop(0)
        except IndexError:
            img = self._next_image()

        if img:
            self._last_video_timestamp = img.timestamp
            self._force_next_video_image = False
            return img.image

    def _update_texture(self, player, timestamp):
        if not self.video_format:
            return
        if self._last_video_timestamp > timestamp:
            return
        img = None
        i = 0
        while not img or img.timestamp < timestamp and not self._force_next_video_image:
            if self._buffered_images:
                img = self._buffered_images.pop(0)
            else:
                packet = self._get_packet_for_stream(self._video_stream_index)
                if not packet:
                    return
                img = self._decode_video_packet(packet)
            i += 1
            if i > 60:
                break

        if img:
            player._texture.blit_into(img.image, 0, 0, 0)
            self._last_video_timestamp = img.timestamp
            self._force_next_video_image = False
        return

    def _release_texture(self, player):
        player._texture = None
        return


av.avbin_init()
if pyglet.options['debug_media']:
    av.avbin_set_log_level(AVBIN_LOG_DEBUG)
else:
    av.avbin_set_log_level(AVBIN_LOG_QUIET)