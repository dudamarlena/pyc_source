# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/mpeg.py
# Compiled at: 2010-08-12 16:04:10
__all__ = [
 'Parser']
import os, struct, logging, stat, core
log = logging.getLogger('metadata')
START_CODE = {0: 'picture_start_code', 
   176: 'reserved', 
   177: 'reserved', 
   178: 'user_data_start_code', 
   179: 'sequence_header_code', 
   180: 'sequence_error_code', 
   181: 'extension_start_code', 
   182: 'reserved', 
   183: 'sequence end', 
   184: 'group of pictures'}
for i in range(1, 175):
    START_CODE[i] = 'slice_start_code'

PICTURE = 0
USERDATA = 178
SEQ_HEAD = 179
SEQ_ERR = 180
EXT_START = 181
SEQ_END = 183
GOP = 184
SEQ_START_CODE = 179
PACK_PKT = 186
SYS_PKT = 187
PADDING_PKT = 190
AUDIO_PKT = 192
VIDEO_PKT = 224
PRIVATE_STREAM1 = 189
PRIVATE_STREAM2 = 191
TS_PACKET_LENGTH = 188
TS_SYNC = 71
FRAME_RATE = [
 0,
 24000.0 / 1001,
 24,
 25,
 30000.0 / 1001,
 30,
 50,
 60000.0 / 1001,
 60]
ASPECT_RATIO = (
 None,
 1.0,
 4.0 / 3,
 16.0 / 9,
 2.21)

class MPEG(core.AVContainer):
    """
    Parser for various MPEG files. This includes MPEG-1 and MPEG-2
    program streams, elementary streams and transport streams. The
    reported length differs from the length reported by most video
    players but the provides length here is correct. An MPEG file has
    no additional metadata like title, etc; only codecs, length and
    resolution is reported back.
    """

    def __init__(self, file):
        core.AVContainer.__init__(self)
        self.sequence_header_offset = 0
        self.mpeg_version = 2
        if not self.isTS(file):
            if not self.isMPEG(file):
                if not self.isPES(file):
                    if self.isES(file):
                        return
                    if file.name.lower().endswith('mpeg') or file.name.lower().endswith('mpg'):
                        if not self.isMPEG(file, force=True) or not self.video or not self.audio:
                            raise core.ParseError()
                    else:
                        raise core.ParseError()
        self.mime = 'video/mpeg'
        if not self.video:
            self.video.append(core.VideoStream())
        if self.sequence_header_offset <= 0:
            return
        self.progressive(file)
        for vi in self.video:
            vi.width, vi.height = self.dxy(file)
            vi.fps, vi.aspect = self.framerate_aspect(file)
            vi.bitrate = self.bitrate(file)
            if self.length:
                vi.length = self.length

        if not self.type:
            self.type = 'MPEG Video'
        vc, ac = ('MP2V', 'MP2A')
        if self.mpeg_version == 1:
            vc, ac = ('MPEG', 80)
        for v in self.video:
            v.codec = vc

        for a in self.audio:
            if not a.codec:
                a.codec = ac

    def dxy(self, file):
        """
        get width and height of the video
        """
        file.seek(self.sequence_header_offset + 4, 0)
        v = file.read(4)
        x = struct.unpack('>H', v[:2])[0] >> 4
        y = struct.unpack('>H', v[1:3])[0] & 4095
        return (x, y)

    def framerate_aspect(self, file):
        """
        read framerate and aspect ratio
        """
        file.seek(self.sequence_header_offset + 7, 0)
        v = struct.unpack('>B', file.read(1))[0]
        try:
            fps = FRAME_RATE[(v & 15)]
        except IndexError:
            fps = None

        if v >> 4 < len(ASPECT_RATIO):
            aspect = ASPECT_RATIO[(v >> 4)]
        else:
            aspect = None
        return (
         fps, aspect)

    def progressive(self, file):
        """
        Try to find out with brute force if the mpeg is interlaced or not.
        Search for the Sequence_Extension in the extension header (01B5)
        """
        file.seek(0)
        buffer = ''
        count = 0
        while 1:
            if len(buffer) < 1000:
                count += 1
                if count > 1000:
                    break
                buffer += file.read(1024)
            if len(buffer) < 1000:
                break
            pos = buffer.find(b'\x00\x00\x01\xb5')
            if pos == -1 or len(buffer) - pos < 5:
                buffer = buffer[-10:]
                continue
            ext = ord(buffer[(pos + 4)]) >> 4
            if ext == 8:
                pass
            else:
                if ext == 1:
                    if ord(buffer[(pos + 5)]) >> 3 & 1:
                        self._set('progressive', True)
                    else:
                        self._set('interlaced', True)
                    return True
                log.debug('ext', ext)
            buffer = buffer[pos + 4:]

        return False

    def bitrate(self, file):
        """
        read the bitrate (most of the time broken)
        """
        file.seek(self.sequence_header_offset + 8, 0)
        t, b = struct.unpack('>HB', file.read(3))
        vrate = t << 2 | b >> 6
        return vrate * 400

    def ReadSCRMpeg2(self, buffer):
        """
        read SCR (timestamp) for MPEG2 at the buffer beginning (6 Bytes)
        """
        if len(buffer) < 6:
            return None
        else:
            highbit = (ord(buffer[0]) & 32) >> 5
            low4Bytes = (long(ord(buffer[0])) & 24) >> 3 << 30
            low4Bytes |= (ord(buffer[0]) & 3) << 28
            low4Bytes |= ord(buffer[1]) << 20
            low4Bytes |= (ord(buffer[2]) & 248) << 12
            low4Bytes |= (ord(buffer[2]) & 3) << 13
            low4Bytes |= ord(buffer[3]) << 5
            low4Bytes |= ord(buffer[4]) >> 3
            sys_clock_ref = (ord(buffer[4]) & 3) << 7
            sys_clock_ref |= ord(buffer[5]) >> 1
            return (long(highbit * 65536 * 65536) + low4Bytes) / 90000

    def ReadSCRMpeg1(self, buffer):
        """
        read SCR (timestamp) for MPEG1 at the buffer beginning (5 Bytes)
        """
        if len(buffer) < 5:
            return None
        else:
            highbit = ord(buffer[0]) >> 3 & 1
            low4Bytes = (long(ord(buffer[0])) >> 1 & 3) << 30
            low4Bytes |= ord(buffer[1]) << 22
            low4Bytes |= ord(buffer[2]) >> 1 << 15
            low4Bytes |= ord(buffer[3]) << 7
            low4Bytes |= ord(buffer[4]) >> 1
            return (long(highbit) * 65536 * 65536 + low4Bytes) / 90000

    def ReadPTS(self, buffer):
        """
        read PTS (PES timestamp) at the buffer beginning (5 Bytes)
        """
        high = (ord(buffer[0]) & 15) >> 1
        med = (ord(buffer[1]) << 7) + (ord(buffer[2]) >> 1)
        low = (ord(buffer[3]) << 7) + (ord(buffer[4]) >> 1)
        return ((long(high) << 30) + (med << 15) + low) / 90000

    def ReadHeader(self, buffer, offset):
        """
        Handle MPEG header in buffer on position offset
        Return None on error, new offset or 0 if the new offset can't be scanned
        """
        if buffer[offset:offset + 3] != '\x00\x00\x01':
            return None
        else:
            id = ord(buffer[(offset + 3)])
            if id == PADDING_PKT:
                return offset + (ord(buffer[(offset + 4)]) << 8) + ord(buffer[(offset + 5)]) + 6
            if id == PACK_PKT:
                if ord(buffer[(offset + 4)]) & 240 == 32:
                    self.type = 'MPEG-1 Video'
                    self.get_time = self.ReadSCRMpeg1
                    self.mpeg_version = 1
                    return offset + 12
                else:
                    if ord(buffer[(offset + 4)]) & 192 == 64:
                        self.type = 'MPEG-2 Video'
                        self.get_time = self.ReadSCRMpeg2
                        return offset + (ord(buffer[(offset + 13)]) & 7) + 14
                    return 0

            if 192 <= id <= 223:
                for a in self.audio:
                    if a.id == id:
                        break
                else:
                    self.audio.append(core.AudioStream())
                    self.audio[(-1)]._set('id', id)

                return 0
            if 224 <= id <= 239:
                for v in self.video:
                    if v.id == id:
                        break
                else:
                    self.video.append(core.VideoStream())
                    self.video[(-1)]._set('id', id)

                return 0
            if id == SEQ_HEAD:
                self.sequence_header_offset = offset
                return 0
            if id in (PRIVATE_STREAM1, PRIVATE_STREAM2):
                add = ord(buffer[(offset + 8)])
                if buffer[offset + 11 + add:offset + 15 + add].find('\x0bw') != -1:
                    for a in self.audio:
                        if a.id == id:
                            break
                    else:
                        self.audio.append(core.AudioStream())
                        self.audio[(-1)]._set('id', id)
                        self.audio[(-1)].codec = 8192

                return 0
            if id == SYS_PKT:
                return 0
            if id == EXT_START:
                return 0
            return 0

    def isMPEG(self, file, force=False):
        """
        This MPEG starts with a sequence of 0x00 followed by a PACK Header
        http://dvd.sourceforge.net/dvdinfo/packhdr.html
        """
        file.seek(0, 0)
        buffer = file.read(10000)
        offset = 0
        while offset < len(buffer) - 100 and buffer[offset] == '\x00':
            offset += 1

        offset -= 2
        header = '\x00\x00\x01%s' % chr(PACK_PKT)
        if offset < 0 or not buffer[offset:offset + 4] == header:
            if not force:
                return 0
            offset = buffer.find(header)
            if offset < 0:
                return 0
        buffer += file.read(100000)
        self.ReadHeader(buffer, offset)
        self.start = self.get_time(buffer[offset + 4:])
        while len(buffer) > offset + 1000 and buffer[offset:offset + 3] == '\x00\x00\x01':
            new_offset = self.ReadHeader(buffer, offset)
            if new_offset == None:
                return 0
            if new_offset:
                offset = new_offset
                while len(buffer) > offset + 10 and not ord(buffer[(offset + 2)]):
                    offset += 1

            else:
                offset += buffer[offset + 4:].find('\x00\x00\x01') + 4

        self.__seek_size__ = 1000000
        self.__sample_size__ = 10000
        self.__search__ = self._find_timer_
        self.filename = file.name
        self.length = self.get_length()
        return 1

    def _find_timer_(self, buffer):
        """
        Return position of timer in buffer or None if not found.
        This function is valid for 'normal' mpeg files
        """
        pos = buffer.find('\x00\x00\x01%s' % chr(PACK_PKT))
        if pos == -1:
            return None
        else:
            return pos + 4

    def ReadPESHeader(self, offset, buffer, id=0):
        """
        Parse a PES header.
        Since it starts with 0x00 0x00 0x01 like 'normal' mpegs, this
        function will return (0, None) when it is no PES header or
        (packet length, timestamp position (maybe None))

        http://dvd.sourceforge.net/dvdinfo/pes-hdr.html
        """
        if not buffer[0:3] == '\x00\x00\x01':
            return (0, None)
        else:
            packet_length = (ord(buffer[4]) << 8) + ord(buffer[5]) + 6
            align = ord(buffer[6]) & 4
            header_length = ord(buffer[8])
            if ord(buffer[3]) & 224 == 192:
                id = id or ord(buffer[3]) & 31
                for a in self.audio:
                    if a.id == id:
                        break
                else:
                    self.audio.append(core.AudioStream())
                    self.audio[(-1)]._set('id', id)

            else:
                if ord(buffer[3]) & 240 == 224:
                    id = id or ord(buffer[3]) & 15
                    for v in self.video:
                        if v.id == id:
                            break
                    else:
                        self.video.append(core.VideoStream())
                        self.video[(-1)]._set('id', id)

                    if buffer[header_length + 9:header_length + 13] == b'\x00\x00\x01\xb3' and not self.sequence_header_offset:
                        self.sequence_header_offset = offset + header_length + 9
                elif ord(buffer[3]) == 189 or ord(buffer[3]) == 191:
                    id = id or ord(buffer[3]) & 15
                    if align and buffer[header_length + 9:header_length + 11] == '\x0bw':
                        for a in self.audio:
                            if a.id == id:
                                break
                        else:
                            self.audio.append(core.AudioStream())
                            self.audio[(-1)]._set('id', id)
                            self.audio[(-1)].codec = 8192

                ptsdts = ord(buffer[7]) >> 6
                if ptsdts and ptsdts == ord(buffer[9]) >> 4:
                    if ord(buffer[9]) >> 4 != ptsdts:
                        log.warning('WARNING: bad PTS/DTS, please contact us')
                        return (
                         packet_length, None)
                    high = (ord(buffer[9]) & 15) >> 1
                    med = (ord(buffer[10]) << 7) + (ord(buffer[11]) >> 1)
                    low = (ord(buffer[12]) << 7) + (ord(buffer[13]) >> 1)
                    return (
                     packet_length, 9)
            return (
             packet_length, None)

    def isPES(self, file):
        log.info('trying mpeg-pes scan')
        file.seek(0, 0)
        buffer = file.read(3)
        if not buffer == '\x00\x00\x01':
            return 0
        else:
            self.sequence_header_offset = 0
            buffer += file.read(10000)
            offset = 0
            while offset + 1000 < len(buffer):
                pos, timestamp = self.ReadPESHeader(offset, buffer[offset:])
                if not pos:
                    return 0
                if timestamp != None and not hasattr(self, 'start'):
                    self.get_time = self.ReadPTS
                    bpos = buffer[offset + timestamp:offset + timestamp + 5]
                    self.start = self.get_time(bpos)
                if self.sequence_header_offset and hasattr(self, 'start'):
                    break
                offset += pos
                if offset + 1000 < len(buffer) and len(buffer) < 1000000 or 1:
                    buffer += file.read(10000)

            if not self.video and not self.audio:
                return 0
            self.type = 'MPEG-PES'
            self.__seek_size__ = 10000000
            self.__sample_size__ = 500000
            self.__search__ = self._find_timer_PES_
            self.filename = file.name
            self.length = self.get_length()
            return 1

    def _find_timer_PES_(self, buffer):
        """
        Return position of timer in buffer or -1 if not found.
        This function is valid for PES files
        """
        pos = buffer.find('\x00\x00\x01')
        offset = 0
        if pos == -1 or offset + 1000 >= len(buffer):
            return
        retpos = -1
        ackcount = 0
        while offset + 1000 < len(buffer):
            pos, timestamp = self.ReadPESHeader(offset, buffer[offset:])
            if timestamp != None and retpos == -1:
                retpos = offset + timestamp
            if pos == 0:
                offset += buffer[offset:].find('\x00\x00\x01')
                retpos = -1
                ackcount = 0
            else:
                offset += pos
                if retpos != -1:
                    ackcount += 1
                if ackcount > 10:
                    return retpos

        return

    def isES(self, file):
        file.seek(0, 0)
        try:
            header = struct.unpack('>LL', file.read(8))
        except (struct.error, IOError):
            return False

        if header[0] != 435:
            return False
        self.mime = 'video/mpeg'
        video = core.VideoStream()
        video.width = header[1] >> 20
        video.height = header[1] >> 8 & 4095
        if header[1] & 15 < len(FRAME_RATE):
            video.fps = FRAME_RATE[(header[1] & 15)]
        if header[1] >> 4 & 15 < len(ASPECT_RATIO):
            video.aspect = ASPECT_RATIO[(header[1] >> 4 & 15)]
        self.video.append(video)
        return True

    def isTS(self, file):
        file.seek(0, 0)
        buffer = file.read(TS_PACKET_LENGTH * 2)
        c = 0
        while c + TS_PACKET_LENGTH < len(buffer):
            if ord(buffer[c]) == ord(buffer[(c + TS_PACKET_LENGTH)]) == TS_SYNC:
                break
            c += 1
        else:
            return 0

        buffer += file.read(10000)
        self.type = 'MPEG-TS'
        while c + TS_PACKET_LENGTH < len(buffer):
            start = ord(buffer[(c + 1)]) & 64
            if c + 2 * TS_PACKET_LENGTH > len(buffer) and c < 500000:
                buffer += file.read(10000)
            if not start:
                c += TS_PACKET_LENGTH
                continue
            pid = (ord(buffer[(c + 1)]) & 31) << 8 | ord(buffer[(c + 2)])
            tsid = ((ord(buffer[(c + 1)]) & 63) << 8) + ord(buffer[(c + 2)])
            adapt = (ord(buffer[(c + 3)]) & 48) >> 4
            afc = ord(buffer[(c + 3)]) >> 4 & 3
            offset = 4
            if adapt & 2:
                adapt_len = ord(buffer[(c + offset)])
                offset += adapt_len + 1
            if not ord(buffer[(c + 1)]) & 64:
                pass
            elif adapt & 1:
                timestamp = self.ReadPESHeader(c + offset, buffer[c + offset:], tsid)[1]
                if timestamp != None:
                    if not hasattr(self, 'start'):
                        self.get_time = self.ReadPTS
                        timestamp = c + offset + timestamp
                        self.start = self.get_time(buffer[timestamp:timestamp + 5])
                    elif not hasattr(self, 'audio_ok'):
                        timestamp = c + offset + timestamp
                        start = self.get_time(buffer[timestamp:timestamp + 5])
                        if start is not None and self.start is not None and abs(start - self.start) < 10:
                            self.audio_ok = True
                        else:
                            del self.start
                            log.warning('Timestamp error, correcting')
            if hasattr(self, 'start') and self.start and self.sequence_header_offset and self.video and self.audio:
                break
            c += TS_PACKET_LENGTH

        if not self.sequence_header_offset:
            return 0
        else:
            self.__seek_size__ = 10000000
            self.__sample_size__ = 100000
            self.__search__ = self._find_timer_TS_
            self.filename = file.name
            self.length = self.get_length()
            return 1

    def _find_timer_TS_(self, buffer):
        c = 0
        while c + TS_PACKET_LENGTH < len(buffer):
            if ord(buffer[c]) == ord(buffer[(c + TS_PACKET_LENGTH)]) == TS_SYNC:
                break
            c += 1
        else:
            return

        while c + TS_PACKET_LENGTH < len(buffer):
            start = ord(buffer[(c + 1)]) & 64
            if not start:
                c += TS_PACKET_LENGTH
                continue
            tsid = ((ord(buffer[(c + 1)]) & 63) << 8) + ord(buffer[(c + 2)])
            adapt = (ord(buffer[(c + 3)]) & 48) >> 4
            offset = 4
            if adapt & 2:
                offset += ord(buffer[(c + offset)]) + 1
            if adapt & 1:
                timestamp = self.ReadPESHeader(c + offset, buffer[c + offset:], tsid)[1]
                if timestamp is None:
                    log.error('bad TS')
                    return
                return c + offset + timestamp
            c += TS_PACKET_LENGTH

        return

    def get_endpos(self):
        """
        get the last timestamp of the mpeg, return -1 if this is not possible
        """
        if not hasattr(self, 'filename') or not hasattr(self, 'start'):
            return
        length = os.stat(self.filename)[stat.ST_SIZE]
        if length < self.__sample_size__:
            return
        else:
            file = open(self.filename)
            file.seek(length - self.__sample_size__)
            buffer = file.read(self.__sample_size__)
            end = None
            while 1:
                pos = self.__search__(buffer)
                if pos == None:
                    break
                end = self.get_time(buffer[pos:]) or end
                buffer = buffer[pos + 100:]

            file.close()
            return end

    def get_length(self):
        """
        get the length in seconds, return -1 if this is not possible
        """
        end = self.get_endpos()
        if end == None or self.start == None:
            return
        if self.start > end:
            return int(((long(1) << 33) - 1) / 90000) - self.start + end
        else:
            return end - self.start

    def seek(self, end_time):
        """
        Return the byte position in the file where the time position
        is 'pos' seconds. Return 0 if this is not possible
        """
        if not hasattr(self, 'filename') or not hasattr(self, 'start'):
            return 0
        file = open(self.filename)
        seek_to = 0
        while 1:
            file.seek(self.__seek_size__, 1)
            buffer = file.read(self.__sample_size__)
            if len(buffer) < 10000:
                break
            pos = self.__search__(buffer)
            if pos != None:
                nt = self.get_time(buffer[pos:])
                if nt is not None and nt >= end_time:
                    break
            seek_to = file.tell()

        file.close()
        return seek_to

    def __scan__(self):
        """
        scan file for timestamps (may take a long time)
        """
        if not hasattr(self, 'filename') or not hasattr(self, 'start'):
            return 0
        file = open(self.filename)
        log.debug('scanning file...')
        while 1:
            file.seek(self.__seek_size__ * 10, 1)
            buffer = file.read(self.__sample_size__)
            if len(buffer) < 10000:
                break
            pos = self.__search__(buffer)
            if pos == None:
                continue
            log.debug('buffer position: %s' % self.get_time(buffer[pos:]))

        file.close()
        log.debug('done scanning file')
        return


Parser = MPEG