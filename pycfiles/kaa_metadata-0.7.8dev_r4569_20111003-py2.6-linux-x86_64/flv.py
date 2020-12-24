# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/flv.py
# Compiled at: 2009-05-22 11:00:08
__all__ = [
 'Parser']
import sys, struct, logging, core
log = logging.getLogger('metadata')
FLV_TAG_TYPE_AUDIO = 8
FLV_TAG_TYPE_VIDEO = 9
FLV_TAG_TYPE_META = 18
FLV_AUDIO_CHANNEL_MASK = 1
FLV_AUDIO_SAMPLERATE_MASK = 12
FLV_AUDIO_CODECID_MASK = 240
FLV_AUDIO_SAMPLERATE_OFFSET = 2
FLV_AUDIO_CODECID_OFFSET = 4
FLV_AUDIO_CODECID = (1, 2, 85, 1)
FLV_VIDEO_CODECID_MASK = 15
FLV_VIDEO_CODECID = ('FLV1', 'MSS1', 'VP60')
FLV_DATA_TYPE_NUMBER = 0
FLV_DATA_TYPE_BOOL = 1
FLV_DATA_TYPE_STRING = 2
FLV_DATA_TYPE_OBJECT = 3
FLC_DATA_TYPE_CLIP = 4
FLV_DATA_TYPE_REFERENCE = 7
FLV_DATA_TYPE_ECMARRAY = 8
FLV_DATA_TYPE_ENDOBJECT = 9
FLV_DATA_TYPE_ARRAY = 10
FLV_DATA_TYPE_DATE = 11
FLV_DATA_TYPE_LONGSTRING = 12
FLVINFO = {'creator': 'copyright'}

class FlashVideo(core.AVContainer):
    """
    Experimental parser for Flash videos. It requires certain flags to
    be set to report video resolutions and in most cases it does not
    provide that information.
    """
    table_mapping = {'FLVINFO': FLVINFO}

    def __init__(self, file):
        core.AVContainer.__init__(self)
        self.mime = 'video/flv'
        self.type = 'Flash Video'
        data = file.read(13)
        if len(data) < 13 or struct.unpack('>3sBBII', data)[0] != 'FLV':
            raise core.ParseError()
        for i in range(10):
            if self.audio and self.video:
                break
            data = file.read(11)
            if len(data) < 11:
                break
            chunk = struct.unpack('>BH4BI', data)
            size = (chunk[1] << 8) + chunk[2]
            if chunk[0] == FLV_TAG_TYPE_AUDIO:
                flags = ord(file.read(1))
                if not self.audio:
                    a = core.AudioStream()
                    a.channels = (flags & FLV_AUDIO_CHANNEL_MASK) + 1
                    srate = flags & FLV_AUDIO_SAMPLERATE_MASK
                    a.samplerate = 44100 << (srate >> FLV_AUDIO_SAMPLERATE_OFFSET) >> 3
                    codec = (flags & FLV_AUDIO_CODECID_MASK) >> FLV_AUDIO_CODECID_OFFSET
                    if codec < len(FLV_AUDIO_CODECID):
                        a.codec = FLV_AUDIO_CODECID[codec]
                    self.audio.append(a)
                file.seek(size - 1, 1)
            elif chunk[0] == FLV_TAG_TYPE_VIDEO:
                flags = ord(file.read(1))
                if not self.video:
                    v = core.VideoStream()
                    codec = (flags & FLV_VIDEO_CODECID_MASK) - 2
                    if codec < len(FLV_VIDEO_CODECID):
                        v.codec = FLV_VIDEO_CODECID[codec]
                    self.video.append(v)
                file.seek(size - 1, 1)
            elif chunk[0] == FLV_TAG_TYPE_META:
                log.info('metadata %s', str(chunk))
                metadata = file.read(size)
                try:
                    while metadata:
                        length, value = self._parse_value(metadata)
                        if isinstance(value, dict):
                            log.info('metadata: %s', value)
                            if value.get('creator'):
                                self.copyright = value.get('creator')
                            if value.get('width'):
                                self.width = value.get('width')
                            if value.get('height'):
                                self.height = value.get('height')
                            if value.get('duration'):
                                self.length = value.get('duration')
                            self._appendtable('FLVINFO', value)
                        if not length:
                            break
                        metadata = metadata[length:]

                except (IndexError, struct.error, TypeError):
                    pass

            else:
                log.info('unkown %s', str(chunk))
                file.seek(size, 1)
            file.seek(4, 1)

    def _parse_value(self, data):
        """
        Parse the next metadata value.
        """
        if ord(data[0]) == FLV_DATA_TYPE_NUMBER:
            value = struct.unpack('>d', data[1:9])[0]
            return (
             9, value)
        else:
            if ord(data[0]) == FLV_DATA_TYPE_BOOL:
                return (2, bool(data[1]))
            if ord(data[0]) == FLV_DATA_TYPE_STRING:
                length = (ord(data[1]) << 8) + ord(data[2])
                return (
                 length + 3, data[3:length + 3])
            if ord(data[0]) == FLV_DATA_TYPE_ECMARRAY:
                init_length = len(data)
                num = struct.unpack('>I', data[1:5])[0]
                data = data[5:]
                result = {}
                for i in range(num):
                    length = (ord(data[0]) << 8) + ord(data[1])
                    key = data[2:length + 2]
                    data = data[length + 2:]
                    length, value = self._parse_value(data)
                    if not length:
                        return (0, result)
                    result[key] = value
                    data = data[length:]

                return (init_length - len(data), result)
            log.info('unknown code: %x. Stop metadata parser', ord(data[0]))
            return (0, None)


Parser = FlashVideo