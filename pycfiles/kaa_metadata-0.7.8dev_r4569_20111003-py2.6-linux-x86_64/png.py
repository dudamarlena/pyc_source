# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/image/png.py
# Compiled at: 2008-02-13 18:32:00
__all__ = [
 'Parser']
import struct, zlib, logging, kaa, core
log = logging.getLogger('metadata')
PNGSIGNATURE = b'\x89PNG\r\n\x1a\n'

class PNG(core.Image):

    def __init__(self, file):
        core.Image.__init__(self)
        self.mime = 'image/png'
        self.type = 'PNG image'
        signature = file.read(8)
        if signature != PNGSIGNATURE:
            raise core.ParseError()
        self.meta = {}
        while self._readChunk(file):
            pass

        if len(self.meta.keys()):
            self._appendtable('PNGMETA', self.meta)
        for (key, value) in self.meta.items():
            if key.startswith('Thumb:') or key == 'Software':
                self._set(key, value)

    def _readChunk(self, file):
        try:
            (length, type) = struct.unpack('>I4s', file.read(8))
        except (OSError, IOError, struct.error):
            return 0

        key = None
        if type == 'IEND':
            return 0
        else:
            if type == 'IHDR':
                data = file.read(length + 4)
                (self.width, self.height, self.depth) = struct.unpack('>IIb', data[:9])
            elif type == 'tEXt':
                log.debug('latin-1 Text found.')
                (data, crc) = struct.unpack('>%isI' % length, file.read(length + 4))
                (key, value) = data.split('\x00')
                self.meta[key] = kaa.str_to_unicode(value)
            elif type == 'zTXt':
                log.debug('Compressed Text found.')
                (data, crc) = struct.unpack('>%isI' % length, file.read(length + 4))
                split = data.split('\x00')
                key = split[0]
                value = ('').join(split[1:])
                compression = ord(value[0])
                value = value[1:]
                if compression == 0:
                    decompressed = zlib.decompress(value)
                    log.debug('%s (Compressed %i) -> %s' % (
                     key, compression, decompressed))
                else:
                    log.debug('%s has unknown Compression %c' % (key, compression))
                self.meta[key] = kaa.str_to_unicode(value)
            elif type == 'iTXt':
                log.debug('International Text found.')
                (data, crc) = struct.unpack('>%isI' % length, file.read(length + 4))
                (key, value) = data.split('\x00')
                self.meta[key] = kaa.str_to_unicode(value)
            else:
                file.seek(length + 4, 1)
                log.debug('%s of length %d ignored.' % (type, length))
            if key is not None and key.lower() == 'comment':
                self.comment = self.meta[key]
            return 1


Parser = PNG