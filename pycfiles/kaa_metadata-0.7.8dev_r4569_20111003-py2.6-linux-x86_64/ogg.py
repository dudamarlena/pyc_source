# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/ogg.py
# Compiled at: 2009-02-02 09:52:25
__all__ = [
 'Parser']
import re, os, stat, struct, logging, core
log = logging.getLogger('metadata')
VORBIS_PACKET_INFO = '\x01vorbis'
VORBIS_PACKET_HEADER = '\x03vorbis'
VORBIS_PACKET_SETUP = '\x05vorbis'

class Ogg(core.Music):

    def __init__(self, file):
        core.Music.__init__(self)
        h = file.read(27)
        if h[:5] != 'OggS\x00':
            log.info('Invalid header')
            raise core.ParseError()
        if ord(h[5]) != 2:
            log.info('Invalid header type flag (trying to go ahead anyway)')
        self.pageSegCount = ord(h[(-1)])
        file.seek(self.pageSegCount, 1)
        h = file.read(7)
        if h != VORBIS_PACKET_INFO:
            log.info('Wrong vorbis header type, giving up.')
            raise core.ParseError()
        self.mime = 'audio/x-vorbis+ogg'
        header = {}
        info = file.read(23)
        self.version, self.channels, self.samplerate, bitrate_max, self.bitrate, bitrate_min, blocksize, framing = struct.unpack('<IBIiiiBB', info[:23])
        self.bitrate = self.bitrate / 1000
        h = file.read(27)
        if h[:4] == 'OggS':
            serial, pagesequence, checksum, numEntries = struct.unpack('<14xIIIB', h)
            file.seek(numEntries, 1)
            h = file.read(7)
            if h != VORBIS_PACKET_HEADER:
                return
            self.encoder = self._extractHeaderString(file)
            numItems = struct.unpack('<I', file.read(4))[0]
            for i in range(numItems):
                s = self._extractHeaderString(file)
                a = re.split('=', s)
                header[a[0].upper()] = a[1]

            if header.has_key('TITLE'):
                self.title = header['TITLE']
            if header.has_key('ALBUM'):
                self.album = header['ALBUM']
            if header.has_key('ARTIST'):
                self.artist = header['ARTIST']
            if header.has_key('COMMENT'):
                self.comment = header['COMMENT']
            if header.has_key('DATE'):
                self.userdate = header['DATE']
            if header.has_key('ENCODER'):
                self.encoder = header['ENCODER']
            if header.has_key('TRACKNUMBER'):
                self.trackno = header['TRACKNUMBER']
            self.type = 'OGG Vorbis'
            self.subtype = ''
            self.length = self._calculateTrackLength(file)
            self._appendtable('VORBISCOMMENT', header)

    def _extractHeaderString(self, f):
        len = struct.unpack('<I', f.read(4))[0]
        return unicode(f.read(len), 'utf-8')

    def _calculateTrackLength(self, f):
        if os.stat(f.name)[stat.ST_SIZE] > 20000:
            f.seek(os.stat(f.name)[stat.ST_SIZE] - 10000)
        h = f.read()
        granule_position = 0
        if len(h):
            idx = h.rfind('OggS')
            if idx < 0:
                return 0
            pageSize = 0
            h = h[idx + 4:]
            check, type, granule_position, absPos, serial, pageN, crc, segs = struct.unpack('<BBIIIIIB', h[:23])
            if check != 0:
                log.debug(h[:10])
                return
            log.debug('granule = %d / %d' % (granule_position, absPos))
        return float(granule_position) / self.samplerate


Parser = Ogg