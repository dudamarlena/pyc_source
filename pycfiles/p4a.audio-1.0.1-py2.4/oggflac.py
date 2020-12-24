# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/thirdparty/mutagen/oggflac.py
# Compiled at: 2007-11-27 08:43:15
"""Read and write Ogg FLAC comments.

This module handles FLAC files wrapped in an Ogg bitstream. The first
FLAC stream found is used. For 'naked' FLACs, see mutagen.flac.

This module is bsaed off the specification at
http://flac.sourceforge.net/ogg_mapping.html.
"""
__all__ = [
 'OggFLAC', 'Open', 'delete']
import struct
from cStringIO import StringIO
from mutagen.flac import StreamInfo, VCFLACDict
from mutagen.ogg import OggPage, OggFileType, error as OggError

class error(OggError):
    __module__ = __name__


class OggFLACHeaderError(error):
    __module__ = __name__


class OggFLACStreamInfo(StreamInfo):
    """Ogg FLAC general header and stream info.

    This encompasses the Ogg wrapper for the FLAC STREAMINFO metadata
    block, as well as the Ogg codec setup that precedes it.

    Attributes (in addition to StreamInfo's):
    packets -- number of metadata packets
    serial -- Ogg logical stream serial number
    """
    __module__ = __name__
    packets = 0
    serial = 0

    def load(self, data):
        page = OggPage(data)
        while not page.packets[0].startswith('\x7fFLAC'):
            page = OggPage(data)

        (major, minor, self.packets, flac) = struct.unpack('>BBH4s', page.packets[0][5:13])
        if flac != 'fLaC':
            raise OggFLACHeaderError('invalid FLAC marker (%r)' % flac)
        elif (
         major, minor) != (1, 0):
            raise OggFLACHeaderError('unknown mapping version: %d.%d' % (major, minor))
        self.serial = page.serial
        stringobj = StringIO(page.packets[0][17:])
        super(OggFLACStreamInfo, self).load(StringIO(page.packets[0][17:]))

    def pprint(self):
        return 'Ogg ' + super(OggFLACStreamInfo, self).pprint()


class OggFLACVComment(VCFLACDict):
    __module__ = __name__

    def load(self, data, info, errors='replace'):
        pages = []
        complete = False
        while not complete:
            page = OggPage(data)
            if page.serial == info.serial:
                pages.append(page)
                complete = page.complete or len(page.packets) > 1

        comment = StringIO(OggPage.to_packets(pages)[0][4:])
        super(OggFLACVComment, self).load(comment, errors=errors)

    def _inject(self, fileobj):
        """Write tag data into the FLAC Vorbis comment packet/page."""
        fileobj.seek(0)
        page = OggPage(fileobj)
        while not page.packets[0].startswith('\x7fFLAC'):
            page = OggPage(fileobj)

        first_page = page
        while not (page.sequence == 1 and page.serial == first_page.serial):
            page = OggPage(fileobj)

        old_pages = [page]
        while not (old_pages[(-1)].complete or len(old_pages[(-1)].packets) > 1):
            page = OggPage(fileobj)
            if page.serial == first_page.serial:
                old_pages.append(page)

        packets = OggPage.to_packets(old_pages, strict=False)
        data = self.write()
        data = packets[0][0] + struct.pack('>I', len(data))[-3:] + data
        packets[0] = data
        new_pages = OggPage.from_packets(packets, old_pages[0].sequence)
        OggPage.replace(fileobj, old_pages, new_pages)


class OggFLAC(OggFileType):
    """An Ogg FLAC file."""
    __module__ = __name__
    _Info = OggFLACStreamInfo
    _Tags = OggFLACVComment
    _Error = OggFLACHeaderError

    def score(filename, fileobj, header):
        return header.startswith('OggS') * (('FLAC' in header) + ('fLaC' in header))

    score = staticmethod(score)


Open = OggFLAC

def delete(filename):
    """Remove tags from a file."""
    OggFLAC(filename).delete()