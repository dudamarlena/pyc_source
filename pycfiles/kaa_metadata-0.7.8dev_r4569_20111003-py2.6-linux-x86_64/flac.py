# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/flac.py
# Compiled at: 2008-03-23 13:53:26
__all__ = [
 'Parser']
import struct, re, logging, core
log = logging.getLogger('metadata')

class Flac(core.Music):

    def __init__(self, file):
        core.Music.__init__(self)
        if file.read(4) != 'fLaC':
            raise core.ParseError()
        self.mime = 'application/flac'
        while 1:
            blockheader, = struct.unpack('>I', file.read(4))
            lastblock = blockheader >> 31 & 1
            type = blockheader >> 24 & 127
            numbytes = blockheader & 16777215
            log.debug('Last?: %d, NumBytes: %d, Type: %d' % (
             lastblock, numbytes, type))
            data = file.read(numbytes)
            if type == 0:
                bits = struct.unpack('>L', data[10:14])[0]
                self.samplerate = bits >> 12 & 1048575
                self.channels = (bits >> 9 & 7) + 1
                self.samplebits = (bits >> 4 & 31) + 1
                md5 = data[18:34]
                samples = ((ord(data[13]) & 15) << 32) + struct.unpack('>L', data[14:18])[0]
                self.length = float(samples) / self.samplerate
            elif type == 1:
                pass
            elif type == 2:
                pass
            elif type == 3:
                pass
            elif type == 4:
                skip, self.vendor = self._extractHeaderString(data)
                num, = struct.unpack('<I', data[skip:skip + 4])
                start = skip + 4
                header = {}
                for i in range(num):
                    nextlen, s = self._extractHeaderString(data[start:])
                    start += nextlen
                    a = re.split('=', s)
                    header[a[0].upper()] = a[1]

                map = {'TITLE': 'title', 
                   'ALBUM': 'album', 'ARTIST': 'artist', 'COMMENT': 'comment', 'ENCODER': 'encoder', 
                   'TRACKNUMBER': 'trackno', 'TRACKTOTAL': 'trackof', 'DATE': 'userdate'}
                for key, attr in map.items():
                    if key in header:
                        setattr(self, attr, header[key])

                self._appendtable('VORBISCOMMENT', header)
            elif type == 5:
                pass
            if lastblock:
                break

    def _extractHeaderString(self, header):
        len = struct.unpack('<I', header[:4])[0]
        return (len + 4, unicode(header[4:4 + len], 'utf-8'))


Parser = Flac