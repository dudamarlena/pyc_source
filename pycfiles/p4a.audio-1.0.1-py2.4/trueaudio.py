# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/thirdparty/mutagen/trueaudio.py
# Compiled at: 2007-11-27 08:43:15
"""True Audio audio stream information and tags.

True Audio is a lossless format designed for real-time encoding and
decoding. This module is based on the documentation at
http://www.true-audio.com/TTA_Lossless_Audio_Codec_-_Format_Description

True Audio files use ID3 tags.
"""
__all__ = [
 'TrueAudio', 'Open', 'delete']
from mutagen.id3 import ID3FileType
from mutagen._util import cdata

class error(RuntimeError):
    __module__ = __name__


class TrueAudioHeaderError(error, IOError):
    __module__ = __name__


class TrueAudioInfo(object):
    """True Audio stream information.

    Attributes:
    length - audio length, in seconds
    sample_rate - audio sample rate, in Hz
    """
    __module__ = __name__

    def __init__(self, fileobj, offset):
        fileobj.seek(offset or 0)
        header = fileobj.read(18)
        if len(header) != 18 or not header.startswith('TTA'):
            raise TrueAudioHeaderError('TTA header not found')
        self.sample_rate = cdata.int_le(header[10:14])
        samples = cdata.uint_le(header[14:18])
        self.length = float(samples) / self.sample_rate

    def pprint(self):
        return 'True Audio, %.2f seconds, %d Hz.' % (self.length, self.sample_rate)


class TrueAudio(ID3FileType):
    """A True Audio file."""
    __module__ = __name__
    _Info = TrueAudioInfo

    def score(filename, fileobj, header):
        return header.startswith('ID3') + header.startswith('TTA') + filename.lower().endswith('.tta')

    score = staticmethod(score)


Open = TrueAudio

def delete(filename):
    """Remove tags from a file."""
    TrueAudio(filename).delete()