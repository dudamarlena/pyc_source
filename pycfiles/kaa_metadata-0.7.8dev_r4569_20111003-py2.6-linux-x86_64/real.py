# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/real.py
# Compiled at: 2010-08-22 17:16:03
__all__ = [
 'Parser']
import struct, logging, core
log = logging.getLogger('metadata')

class RealVideo(core.AVContainer):

    def __init__(self, file):
        core.AVContainer.__init__(self)
        self.mime = 'video/real'
        self.type = 'Real Video'
        h = file.read(10)
        try:
            object_id, object_size, object_version = struct.unpack('>4sIH', h)
        except struct.error:
            raise core.ParseError()

        if not object_id == '.RMF':
            raise core.ParseError()
        file_version, num_headers = struct.unpack('>II', file.read(8))
        log.debug('size: %d, ver: %d, headers: %d' % (
         object_size, file_version, num_headers))
        for i in range(0, num_headers):
            try:
                oi = struct.unpack('>4sIH', file.read(10))
            except (struct.error, IOError):
                break

            if object_id == 'DATA' and oi[0] != 'INDX':
                log.debug('INDX chunk expected after DATA but not found -- file corrupt')
                break
            object_id, object_size, object_version = oi
            if object_id == 'DATA':
                file.seek(object_size - 10, 1)
            else:
                self._read_header(object_id, file.read(object_size - 10))
            log.debug('%s [%d]' % (object_id, object_size - 10))

    def _read_header(self, object_id, s):
        if object_id == 'PROP':
            prop = struct.unpack('>9IHH', s)
            log.debug(prop)
        if object_id == 'MDPR':
            mdpr = struct.unpack('>H7I', s[:30])
            log.debug(mdpr)
            self.length = mdpr[7] / 1000.0
            stream_name_size, = struct.unpack('>B', s[30:31])
            stream_name = s[31:31 + stream_name_size]
            pos = 31 + stream_name_size
            mime_type_size, = struct.unpack('>B', s[pos:pos + 1])
            mime = s[pos + 1:pos + 1 + mime_type_size]
            pos += mime_type_size + 1
            type_specific_len, = struct.unpack('>I', s[pos:pos + 4])
            type_specific = s[pos + 4:pos + 4 + type_specific_len]
            pos += 4 + type_specific_len
            if mime[:5] == 'audio':
                ai = core.AudioStream()
                ai.id = mdpr[0]
                ai.bitrate = mdpr[2]
                self.audio.append(ai)
            elif mime[:5] == 'video':
                vi = core.VideoStream()
                vi.id = mdpr[0]
                vi.bitrate = mdpr[2]
                self.video.append(vi)
            else:
                log.debug('Unknown: %s' % mime)
        if object_id == 'CONT':
            pos = 0
            title_len, = struct.unpack('>H', s[pos:pos + 2])
            self.title = s[2:title_len + 2]
            pos += title_len + 2
            author_len, = struct.unpack('>H', s[pos:pos + 2])
            self.artist = s[pos + 2:pos + author_len + 2]
            pos += author_len + 2
            copyright_len, = struct.unpack('>H', s[pos:pos + 2])
            self.copyright = s[pos + 2:pos + copyright_len + 2]
            pos += copyright_len + 2
            comment_len, = struct.unpack('>H', s[pos:pos + 2])
            self.comment = s[pos + 2:pos + comment_len + 2]


Parser = RealVideo