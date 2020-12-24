# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/thirdparty/mutagen/mp3.py
# Compiled at: 2007-11-27 08:43:15
"""MPEG audio stream information and tags."""
import os, struct
from mutagen.id3 import ID3FileType, BitPaddedInt

class error(RuntimeError):
    __module__ = __name__


class HeaderNotFoundError(error, IOError):
    __module__ = __name__


class InvalidMPEGHeader(error, IOError):
    __module__ = __name__


class MPEGInfo(object):
    """MPEG audio stream information

    Parse information about an MPEG audio file. This also reads the
    Xing VBR header format.

    This code was implemented based on the format documentation at
    http://www.dv.co.yu/mpgscript/mpeghdr.htm.

    Useful attributes:
    length -- audio length, in seconds
    bitrate -- audio bitrate, in bits per second
    sketchy -- if true, the file may not be valid MPEG audio

    Useless attributes:
    version -- MPEG version (1, 2, 2.5)
    layer -- 1, 2, or 3
    protected -- whether or not the file is "protected"
    padding -- whether or not audio frames are padded
    sample_rate -- audio sample rate, in Hz
    """
    __module__ = __name__
    __BITRATE = {(1, 1): range(0, 480, 32), (1, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384], (1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320], (2, 1): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256], (2, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]}
    __BITRATE[(2, 3)] = __BITRATE[(2, 2)]
    for i in range(1, 4):
        __BITRATE[(2.5, i)] = __BITRATE[(2, i)]

    __RATES = {1: [44100, 48000, 32000], 2: [22050, 24000, 16000], 2.5: [11025, 12000, 8000]}
    sketchy = False

    def __init__(self, fileobj, offset=None):
        """Parse MPEG stream information from a file-like object.

        If an offset argument is given, it is used to start looking
        for stream information and Xing headers; otherwise, ID3v2 tags
        will be skipped automatically. A correct offset can make
        loading files significantly faster.
        """
        try:
            size = os.path.getsize(fileobj.name)
        except (IOError, OSError, AttributeError):
            fileobj.seek(0, 2)
            size = fileobj.tell()

        if offset is None:
            fileobj.seek(0, 0)
            idata = fileobj.read(10)
            try:
                (id3, insize) = struct.unpack('>3sxxx4s', idata)
            except struct.error:
                (id3, insize) = ('', 0)
            else:
                insize = BitPaddedInt(insize)
                if id3 == 'ID3' and insize > 0:
                    offset = insize
                else:
                    offset = 0
        for i in [offset, 0.3 * size, 0.6 * size, 0.9 * size]:
            try:
                self.__try(fileobj, int(i), size - offset)
            except error, e:
                pass
            else:
                break
        else:
            self.__try(fileobj, offset, size - offset, False)
            self.sketchy = True

        return

    def __try(self, fileobj, offset, real_size, check_second=True):
        fileobj.seek(offset, 0)
        data = fileobj.read(32768)
        frame_1 = data.find(b'\xff')
        while 0 <= frame_1 <= len(data) - 4:
            frame_data = struct.unpack('>I', data[frame_1:frame_1 + 4])[0]
            if frame_data >> 16 & 224 != 224:
                frame_1 = data.find(b'\xff', frame_1 + 2)
            else:
                version = frame_data >> 19 & 3
                layer = frame_data >> 17 & 3
                protection = frame_data >> 16 & 1
                bitrate = frame_data >> 12 & 15
                sample_rate = frame_data >> 10 & 3
                padding = frame_data >> 9 & 1
                private = frame_data >> 8 & 1
                mode = frame_data >> 6 & 3
                mode_extension = frame_data >> 4 & 3
                copyright = frame_data >> 3 & 1
                original = frame_data >> 2 & 1
                emphasis = frame_data >> 0 & 3
                if version == 1 or layer == 0 or sample_rate == 3 or bitrate == 0 or bitrate == 15:
                    frame_1 = data.find(b'\xff', frame_1 + 2)
                else:
                    break
        else:
            raise HeaderNotFoundError("can't sync to an MPEG frame")

        self.version = [
         2.5, None, 2, 1][version]
        self.layer = 4 - layer
        self.protected = not protection
        self.padding = bool(padding)
        self.bitrate = self.__BITRATE[(self.version, self.layer)][bitrate]
        self.bitrate *= 1000
        self.sample_rate = self.__RATES[self.version][sample_rate]
        if self.layer == 1:
            frame_length = (12 * self.bitrate / self.sample_rate + padding) * 4
            frame_size = 384
        else:
            frame_length = 144 * self.bitrate / self.sample_rate + padding
            frame_size = 1152
        if check_second:
            possible = frame_1 + frame_length
            if possible > len(data) + 4:
                raise HeaderNotFoundError("can't sync to second MPEG frame")
            frame_data = struct.unpack('>H', data[possible:possible + 2])[0]
            if frame_data & 65504 != 65504:
                raise HeaderNotFoundError("can't sync to second MPEG frame")
        frame_count = real_size / float(frame_length)
        samples = frame_size * frame_count
        self.length = samples / self.sample_rate
        fileobj.seek(offset, 0)
        data = fileobj.read(32768)
        try:
            xing = data[:-4].index('Xing')
        except ValueError:
            pass
        else:
            self.sketchy = False
            flags = struct.unpack('>I', data[xing + 4:xing + 8])[0]
            if flags & 1:
                frame_count = struct.unpack('>I', data[xing + 8:xing + 12])[0]
                samples = frame_size * frame_count
                self.length = samples / self.sample_rate or self.length
            if flags & 2:
                bytes = struct.unpack('>I', data[xing + 12:xing + 16])[0]
                self.bitrate = int(bytes * 8 // self.length)

        return

    def pprint(self):
        s = 'MPEG %s layer %d, %d bps, %s Hz, %.2f seconds' % (self.version, self.layer, self.bitrate, self.sample_rate, self.length)
        if self.sketchy:
            s += ' (sketchy)'
        return s


class MP3(ID3FileType):
    """An MPEG audio (usually MPEG-1 Layer 3) file."""
    __module__ = __name__
    _Info = MPEGInfo

    def score(filename, fileobj, header):
        filename = filename.lower()
        return header.startswith('ID3') + filename.endswith('.mp3') + filename.endswith('.mp2') + filename.endswith('.mpg') + filename.endswith('.mpeg')

    score = staticmethod(score)


Open = MP3

def delete(filename):
    """Remove tags from a file."""
    MP3(filename).delete()