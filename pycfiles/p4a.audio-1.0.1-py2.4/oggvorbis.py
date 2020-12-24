# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/thirdparty/mutagen/oggvorbis.py
# Compiled at: 2007-11-27 08:43:15
"""Read and write Ogg Vorbis comments.

This module handles Vorbis files wrapped in an Ogg bitstream. The
first Vorbis stream found is used.

Read more about Ogg Vorbis at http://vorbis.com/. This module is based
on the specification at http://www.xiph.org/vorbis/doc/Vorbis_I_spec.html.
"""
__all__ = [
 'OggVorbis', 'Open', 'delete']
import struct
from p4a.audio.ogg.thirdparty.mutagen._vorbis import VCommentDict
from p4a.audio.ogg.thirdparty.mutagen.ogg import OggPage, OggFileType, error as OggError

class error(OggError):
    __module__ = __name__


class OggVorbisHeaderError(error):
    __module__ = __name__


class OggVorbisInfo(object):
    """Ogg Vorbis stream information.

    Attributes:
    length - file length in seconds, as a float
    bitrate - nominal ('average') bitrate in bits per second, as an int
    """
    __module__ = __name__
    length = 0

    def __init__(self, fileobj):
        page = OggPage(fileobj)
        while not page.packets[0].startswith('\x01vorbis'):
            page = OggPage(fileobj)

        if not page.first:
            raise OggVorbisHeaderError("page has ID header, but doesn't start a stream")
        (self.channels, self.sample_rate, max_bitrate, nominal_bitrate, min_bitrate) = struct.unpack('<B4I', page.packets[0][11:28])
        self.serial = page.serial
        if nominal_bitrate == 0:
            self.bitrate = (max_bitrate + min_bitrate) // 2
        elif max_bitrate and max_bitrate < nominal_bitrate:
            self.bitrate = max_bitrate
        elif min_bitrate > nominal_bitrate:
            self.bitrate = min_bitrate
        else:
            self.bitrate = nominal_bitrate

    def pprint(self):
        return 'Ogg Vorbis, %.2f seconds, %d bps' % (self.length, self.bitrate)


class OggVCommentDict(VCommentDict):
    """Vorbis comments embedded in an Ogg bitstream."""
    __module__ = __name__

    def __init__(self, fileobj, info):
        pages = []
        complete = False
        while not complete:
            page = OggPage(fileobj)
            if page.serial == info.serial:
                pages.append(page)
                complete = page.complete or len(page.packets) > 1

        data = OggPage.to_packets(pages)[0][7:]
        super(OggVCommentDict, self).__init__(data)

    def _inject(self, fileobj):
        """Write tag data into the Vorbis comment packet/page."""
        fileobj.seek(0)
        page = OggPage(fileobj)
        while not page.packets[0].startswith('\x03vorbis'):
            page = OggPage(fileobj)

        old_pages = [page]
        while not (old_pages[(-1)].complete or len(old_pages[(-1)].packets) > 1):
            page = OggPage(fileobj)
            if page.serial == old_pages[0].serial:
                old_pages.append(page)

        packets = OggPage.to_packets(old_pages, strict=False)
        packets[0] = '\x03vorbis' + self.write()
        new_pages = OggPage.from_packets(packets, old_pages[0].sequence)
        OggPage.replace(fileobj, old_pages, new_pages)


class OggVorbis(OggFileType):
    """An Ogg Vorbis file."""
    __module__ = __name__
    _Info = OggVorbisInfo
    _Tags = OggVCommentDict
    _Error = OggVorbisHeaderError

    def score(filename, fileobj, header):
        return header.startswith('OggS') * ('\x01vorbis' in header)

    score = staticmethod(score)


Open = OggVorbis

def delete(filename):
    """Remove tags from a file."""
    OggVorbis(filename).delete()