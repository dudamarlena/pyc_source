# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/mkv.py
# Compiled at: 2011-01-23 12:21:43
__all__ = [
 'Parser']
from struct import unpack
import logging, re
from datetime import datetime
import core
log = logging.getLogger('metadata')
MATROSKA_VIDEO_TRACK = 1
MATROSKA_AUDIO_TRACK = 2
MATROSKA_SUBTITLES_TRACK = 17
MATROSKA_HEADER_ID = 440786851
MATROSKA_TRACKS_ID = 374648427
MATROSKA_CUES_ID = 475249515
MATROSKA_SEGMENT_ID = 408125543
MATROSKA_SEGMENT_INFO_ID = 357149030
MATROSKA_CLUSTER_ID = 524531317
MATROSKA_VOID_ID = 236
MATROSKA_CRC_ID = 191
MATROSKA_TIMECODESCALE_ID = 2807729
MATROSKA_DURATION_ID = 17545
MATROSKA_CRC32_ID = 191
MATROSKA_TIMECODESCALE_ID = 2807729
MATROSKA_MUXING_APP_ID = 19840
MATROSKA_WRITING_APP_ID = 22337
MATROSKA_CODEC_ID = 134
MATROSKA_CODEC_PRIVATE_ID = 25506
MATROSKA_FRAME_DURATION_ID = 2352003
MATROSKA_VIDEO_SETTINGS_ID = 224
MATROSKA_VIDEO_WIDTH_ID = 176
MATROSKA_VIDEO_HEIGHT_ID = 186
MATROSKA_VIDEO_INTERLACED_ID = 154
MATROSKA_VIDEO_DISPLAY_WIDTH_ID = 21680
MATROSKA_VIDEO_DISPLAY_HEIGHT_ID = 21690
MATROSKA_AUDIO_SETTINGS_ID = 225
MATROSKA_AUDIO_SAMPLERATE_ID = 181
MATROSKA_AUDIO_CHANNELS_ID = 159
MATROSKA_TRACK_UID_ID = 29637
MATROSKA_TRACK_NUMBER_ID = 215
MATROSKA_TRACK_TYPE_ID = 131
MATROSKA_TRACK_LANGUAGE_ID = 2274716
MATROSKA_TRACK_OFFSET = 21375
MATROSKA_TRACK_FLAG_DEFAULT_ID = 136
MATROSKA_TRACK_FLAG_ENABLED_ID = 185
MATROSKA_TITLE_ID = 31657
MATROSKA_DATE_UTC_ID = 17505
MATROSKA_NAME_ID = 21358
MATROSKA_CHAPTERS_ID = 272869232
MATROSKA_CHAPTER_UID_ID = 29636
MATROSKA_EDITION_ENTRY_ID = 17849
MATROSKA_CHAPTER_ATOM_ID = 182
MATROSKA_CHAPTER_TIME_START_ID = 145
MATROSKA_CHAPTER_TIME_END_ID = 146
MATROSKA_CHAPTER_FLAG_ENABLED_ID = 17816
MATROSKA_CHAPTER_DISPLAY_ID = 128
MATROSKA_CHAPTER_LANGUAGE_ID = 17276
MATROSKA_CHAPTER_STRING_ID = 133
MATROSKA_ATTACHMENTS_ID = 423732329
MATROSKA_ATTACHED_FILE_ID = 24999
MATROSKA_FILE_DESC_ID = 18046
MATROSKA_FILE_NAME_ID = 18030
MATROSKA_FILE_MIME_TYPE_ID = 18016
MATROSKA_FILE_DATA_ID = 18012
MATROSKA_SEEKHEAD_ID = 290298740
MATROSKA_SEEK_ID = 19899
MATROSKA_SEEKID_ID = 21419
MATROSKA_SEEK_POSITION_ID = 21420
MATROSKA_TAGS_ID = 307544935
MATROSKA_TAG_ID = 29555
MATROSKA_TARGETS_ID = 25536
MATROSKA_TARGET_TYPE_VALUE_ID = 26826
MATROSKA_TARGET_TYPE_ID = 25546
MATRSOKA_TAGS_TRACK_UID_ID = 25541
MATRSOKA_TAGS_EDITION_UID_ID = 25545
MATRSOKA_TAGS_CHAPTER_UID_ID = 25540
MATRSOKA_TAGS_ATTACHMENT_UID_ID = 25542
MATROSKA_SIMPLE_TAG_ID = 26568
MATROSKA_TAG_NAME_ID = 17827
MATROSKA_TAG_LANGUAGE_ID = 17530
MATROSKA_TAG_STRING_ID = 17543
MATROSKA_TAG_BINARY_ID = 17541
FOURCCMap = {'V_THEORA': 'THEO', 
   'V_SNOW': 'SNOW', 
   'V_MPEG4/ISO/ASP': 'MP4V', 
   'V_MPEG4/ISO/AVC': 'AVC1', 
   'A_AC3': 8192, 
   'A_MPEG/L3': 85, 
   'A_MPEG/L2': 80, 
   'A_MPEG/L1': 80, 
   'A_DTS': 8193, 
   'A_PCM/INT/LIT': 1, 
   'A_PCM/FLOAT/IEEE': 3, 
   'A_TTA1': 30625, 
   'A_WAVPACK4': 22358, 
   'A_VORBIS': 26448, 
   'A_FLAC': 61868, 
   'A_AAC': 255, 
   'A_AAC/': 255}

def matroska_date_to_datetime(date):
    """
    Converts a date in Matroska's date format to a python datetime object.
    Returns the given date string if it could not be converted.
    """
    format = re.split('([-:. ])', '%Y-%m-%d %H:%M:%S.%f')
    while format:
        try:
            return datetime.strptime(date, ('').join(format))
        except ValueError:
            format = format[:-2]

    return date


def matroska_bps_to_bitrate(bps):
    """
    Tries to convert a free-form bps string into a bitrate (bits per second).
    """
    m = re.search('([\\d.]+)\\s*(\\D.*)', bps)
    if m:
        bps, suffix = m.groups()
        if 'kbit' in suffix:
            return float(bps) * 1024
        if 'kbyte' in suffix:
            return float(bps) * 1024 * 8
        if 'byte' in suffix:
            return float(bps) * 8
        if 'bps' in suffix or 'bit' in suffix:
            return float(bps)
    if bps.replace('.', '').isdigit():
        if float(bps) < 30000:
            return float(bps) * 1024
        return float(bps)


TAGS_MAP = {'title': (
           'title', None), 
   'subtitle': (
              'caption', None), 
   'comment': (
             'comment', None), 
   'url': (
         'url', None), 
   'artist': (
            'artist', None), 
   'keywords': (
              'keywords', lambda s: [ word.strip() for word in s.split(',') ]), 
   'composer_nationality': (
                          'country', None), 
   'date_released': (
                   'datetime', None), 
   'date_recorded': (
                   'datetime', None), 
   'date_written': (
                  'datetime', None), 
   'encoder': (
             'encoder', None), 
   'bps': (
         'bitrate', matroska_bps_to_bitrate), 
   'part_number': (
                 'trackno', int), 
   'total_parts': (
                 'trackof', int), 
   'copyright': (
               'copyright', None), 
   'genre': (
           'genre', None), 
   'actor': (
           'actors', None), 
   'written_by': (
                'writer', None), 
   'producer': (
              'producer', None), 
   'production_studio': (
                       'studio', None), 
   'law_rating': (
                'rating', None), 
   'summary': (
             'summary', None), 
   'synopsis': (
              'synopsis', None)}

class EbmlEntity():
    """
    This is class that is responsible to handle one Ebml entity as described in
    the Matroska/Ebml spec
    """

    def __init__(self, inbuf):
        self.crc_len = 0
        try:
            self.build_entity(inbuf)
        except IndexError:
            raise core.ParseError()

        while self.get_id() == MATROSKA_CRC32_ID:
            self.crc_len += self.get_total_len()
            inbuf = inbuf[self.get_total_len():]
            self.build_entity(inbuf)

    def build_entity(self, inbuf):
        self.compute_id(inbuf)
        if self.id_len == 0:
            log.debug('EBML entity not found, bad file format')
            raise core.ParseError()
        self.entity_len, self.len_size = self.compute_len(inbuf[self.id_len:])
        self.entity_data = inbuf[self.get_header_len():self.get_total_len()]
        self.ebml_length = self.entity_len
        self.entity_len = min(len(self.entity_data), self.entity_len)
        self.value = 0
        if self.entity_len <= 8:
            for pos, shift in zip(range(self.entity_len), range((self.entity_len - 1) * 8, -1, -8)):
                self.value |= ord(self.entity_data[pos]) << shift

    def add_data(self, data):
        maxlen = self.ebml_length - len(self.entity_data)
        if maxlen <= 0:
            return
        self.entity_data += data[:maxlen]
        self.entity_len = len(self.entity_data)

    def compute_id(self, inbuf):
        self.id_len = 0
        if len(inbuf) < 1:
            return 0
        first = ord(inbuf[0])
        if first & 128:
            self.id_len = 1
            self.entity_id = first
        elif first & 64:
            if len(inbuf) < 2:
                return 0
            self.id_len = 2
            self.entity_id = ord(inbuf[0]) << 8 | ord(inbuf[1])
        elif first & 32:
            if len(inbuf) < 3:
                return 0
            self.id_len = 3
            self.entity_id = ord(inbuf[0]) << 16 | ord(inbuf[1]) << 8 | ord(inbuf[2])
        elif first & 16:
            if len(inbuf) < 4:
                return 0
            self.id_len = 4
            self.entity_id = ord(inbuf[0]) << 24 | ord(inbuf[1]) << 16 | ord(inbuf[2]) << 8 | ord(inbuf[3])
        self.entity_str = inbuf[0:self.id_len]

    def compute_len(self, inbuf):
        if not inbuf:
            return (0, 0)
        i = num_ffs = 0
        len_mask = 128
        len = ord(inbuf[0])
        while not len & len_mask:
            i += 1
            len_mask >>= 1
            if i >= 8:
                return (0, 0)

        len &= len_mask - 1
        if len == len_mask - 1:
            num_ffs += 1
        for p in range(i):
            len = len << 8 | ord(inbuf[(p + 1)])
            if len & 255 == 255:
                num_ffs += 1

        if num_ffs == i + 1:
            len = 0
        return (
         len, i + 1)

    def get_crc_len(self):
        return self.crc_len

    def get_value(self):
        return self.value

    def get_float_value(self):
        if len(self.entity_data) == 4:
            return unpack('!f', self.entity_data)[0]
        if len(self.entity_data) == 8:
            return unpack('!d', self.entity_data)[0]
        return 0.0

    def get_data(self):
        return self.entity_data

    def get_utf8(self):
        return unicode(self.entity_data, 'utf-8', 'replace')

    def get_str(self):
        return unicode(self.entity_data, 'ascii', 'replace')

    def get_id(self):
        return self.entity_id

    def get_str_id(self):
        return self.entity_str

    def get_len(self):
        return self.entity_len

    def get_total_len(self):
        return self.entity_len + self.id_len + self.len_size

    def get_header_len(self):
        return self.id_len + self.len_size


class Matroska(core.AVContainer):
    """
    Matroska video and audio parser. If at least one video stream is
    detected it will set the type to MEDIA_AV.
    """
    media = core.MEDIA_AUDIO

    def __init__(self, file):
        core.AVContainer.__init__(self)
        self.samplerate = 1
        self.file = file
        buffer = file.read(2000)
        if len(buffer) == 0:
            raise core.ParseError()
        header = EbmlEntity(buffer)
        if header.get_id() != MATROSKA_HEADER_ID:
            raise core.ParseError()
        log.debug('HEADER ID found %08X' % header.get_id())
        self.mime = 'application/mkv'
        self.type = 'Matroska'
        self.has_idx = False
        self.objects_by_uid = {}
        self.segment = segment = EbmlEntity(buffer[header.get_total_len():])
        self.segment.offset = header.get_total_len() + segment.get_header_len()
        if segment.get_id() != MATROSKA_SEGMENT_ID:
            log.debug('SEGMENT ID not found %08X' % segment.get_id())
            return
        log.debug('SEGMENT ID found %08X' % segment.get_id())
        try:
            for elem in self.process_one_level(segment):
                if elem.get_id() == MATROSKA_SEEKHEAD_ID:
                    self.process_elem(elem)

        except core.ParseError:
            pass

        if not self.has_idx:
            log.debug('WARNING: file has no index')
            self._set('corrupt', True)

    def process_elem(self, elem):
        elem_id = elem.get_id()
        log.debug('BEGIN: process element %s' % hex(elem_id))
        if elem_id == MATROSKA_SEGMENT_INFO_ID:
            duration = 0
            scalecode = 1000000.0
            for ielem in self.process_one_level(elem):
                ielem_id = ielem.get_id()
                if ielem_id == MATROSKA_TIMECODESCALE_ID:
                    scalecode = ielem.get_value()
                elif ielem_id == MATROSKA_DURATION_ID:
                    duration = ielem.get_float_value()
                elif ielem_id == MATROSKA_TITLE_ID:
                    self.title = ielem.get_utf8()
                elif ielem_id == MATROSKA_DATE_UTC_ID:
                    timestamp = unpack('!q', ielem.get_data())[0] / 1000000000.0
                    self.timestamp = int(timestamp + 978307200)

            self.length = duration * scalecode / 1000000000.0
        elif elem_id == MATROSKA_TRACKS_ID:
            self.process_tracks(elem)
        elif elem_id == MATROSKA_CHAPTERS_ID:
            self.process_chapters(elem)
        elif elem_id == MATROSKA_ATTACHMENTS_ID:
            self.process_attachments(elem)
        elif elem_id == MATROSKA_SEEKHEAD_ID:
            self.process_seekhead(elem)
        elif elem_id == MATROSKA_TAGS_ID:
            self.process_tags(elem)
        elif elem_id == MATROSKA_CUES_ID:
            self.has_idx = True
        log.debug('END: process element %s' % hex(elem_id))
        return True

    def process_seekhead(self, elem):
        for seek_elem in self.process_one_level(elem):
            if seek_elem.get_id() != MATROSKA_SEEK_ID:
                continue
            for sub_elem in self.process_one_level(seek_elem):
                if sub_elem.get_id() == MATROSKA_SEEKID_ID:
                    if sub_elem.get_value() == MATROSKA_CLUSTER_ID:
                        return
                elif sub_elem.get_id() == MATROSKA_SEEK_POSITION_ID:
                    self.file.seek(self.segment.offset + sub_elem.get_value())
                    buffer = self.file.read(100)
                    try:
                        elem = EbmlEntity(buffer)
                    except core.ParseError:
                        continue

                    elem.add_data(self.file.read(elem.ebml_length))
                    self.process_elem(elem)

    def process_tracks(self, tracks):
        tracksbuf = tracks.get_data()
        index = 0
        while index < tracks.get_len():
            trackelem = EbmlEntity(tracksbuf[index:])
            log.debug('ELEMENT %X found' % trackelem.get_id())
            self.process_track(trackelem)
            index += trackelem.get_total_len() + trackelem.get_crc_len()

    def process_one_level(self, item):
        buf = item.get_data()
        index = 0
        while index < item.get_len():
            if len(buf[index:]) == 0:
                break
            elem = EbmlEntity(buf[index:])
            yield elem
            index += elem.get_total_len() + elem.get_crc_len()

    def process_track(self, track):
        elements = [ x for x in self.process_one_level(track) ]
        track_type = [ x.get_value() for x in elements if x.get_id() == MATROSKA_TRACK_TYPE_ID ]
        if not track_type:
            log.debug('Bad track: no type id found')
            return
        else:
            track_type = track_type[0]
            track = None
            if track_type == MATROSKA_VIDEO_TRACK:
                log.debug('Video track found')
                track = self.process_video_track(elements)
            elif track_type == MATROSKA_AUDIO_TRACK:
                log.debug('Audio track found')
                track = self.process_audio_track(elements)
            elif track_type == MATROSKA_SUBTITLES_TRACK:
                log.debug('Subtitle track found')
                track = core.Subtitle()
                track.id = len(self.subtitles)
                self.subtitles.append(track)
                for elem in elements:
                    self.process_track_common(elem, track)

            return

    def process_track_common(self, elem, track):
        elem_id = elem.get_id()
        if elem_id == MATROSKA_TRACK_LANGUAGE_ID:
            track.language = elem.get_str()
            log.debug('Track language found: %s' % track.language)
        elif elem_id == MATROSKA_NAME_ID:
            track.title = elem.get_utf8()
        elif elem_id == MATROSKA_TRACK_NUMBER_ID:
            track.trackno = elem.get_value()
        elif elem_id == MATROSKA_TRACK_FLAG_ENABLED_ID:
            track.enabled = bool(elem.get_value())
        elif elem_id == MATROSKA_TRACK_FLAG_DEFAULT_ID:
            track.default = bool(elem.get_value())
        elif elem_id == MATROSKA_CODEC_ID:
            track.codec = elem.get_str()
        elif elem_id == MATROSKA_CODEC_PRIVATE_ID:
            track.codec_private = elem.get_data()
        elif elem_id == MATROSKA_TRACK_UID_ID:
            self.objects_by_uid[elem.get_value()] = track

    def process_video_track(self, elements):
        track = core.VideoStream()
        track.codec = 'Unknown'
        track.fps = 0
        for elem in elements:
            elem_id = elem.get_id()
            if elem_id == MATROSKA_CODEC_ID:
                track.codec = elem.get_str()
            elif elem_id == MATROSKA_FRAME_DURATION_ID:
                try:
                    track.fps = 1 / (pow(10, -9) * elem.get_value())
                except ZeroDivisionError:
                    pass

            elif elem_id == MATROSKA_VIDEO_SETTINGS_ID:
                d_width = d_height = None
                for settings_elem in self.process_one_level(elem):
                    settings_elem_id = settings_elem.get_id()
                    if settings_elem_id == MATROSKA_VIDEO_WIDTH_ID:
                        track.width = settings_elem.get_value()
                    elif settings_elem_id == MATROSKA_VIDEO_HEIGHT_ID:
                        track.height = settings_elem.get_value()
                    elif settings_elem_id == MATROSKA_VIDEO_DISPLAY_WIDTH_ID:
                        d_width = settings_elem.get_value()
                    elif settings_elem_id == MATROSKA_VIDEO_DISPLAY_HEIGHT_ID:
                        d_height = settings_elem.get_value()
                    elif settings_elem_id == MATROSKA_VIDEO_INTERLACED_ID:
                        value = int(settings_elem.get_value())
                        self._set('interlaced', value)

                if None not in (d_width, d_height):
                    track.aspect = float(d_width) / d_height
            else:
                self.process_track_common(elem, track)

        if track.codec in FOURCCMap:
            track.codec = FOURCCMap[track.codec]
        elif '/' in track.codec and track.codec.split('/')[0] + '/' in FOURCCMap:
            track.codec = FOURCCMap[(track.codec.split('/')[0] + '/')]
        elif track.codec.endswith('FOURCC') and len(track.codec_private or '') == 40:
            track.codec = track.codec_private[16:20]
        elif track.codec.startswith('V_REAL/'):
            track.codec = track.codec[7:]
        elif track.codec.startswith('V_'):
            track.codec = track.codec[2:]
        self.media = core.MEDIA_AV
        track.id = len(self.video)
        self.video.append(track)
        return track

    def process_audio_track(self, elements):
        track = core.AudioStream()
        track.codec = 'Unknown'
        for elem in elements:
            elem_id = elem.get_id()
            if elem_id == MATROSKA_CODEC_ID:
                track.codec = elem.get_str()
            elif elem_id == MATROSKA_AUDIO_SETTINGS_ID:
                for settings_elem in self.process_one_level(elem):
                    settings_elem_id = settings_elem.get_id()
                    if settings_elem_id == MATROSKA_AUDIO_SAMPLERATE_ID:
                        track.samplerate = settings_elem.get_float_value()
                    elif settings_elem_id == MATROSKA_AUDIO_CHANNELS_ID:
                        track.channels = settings_elem.get_value()

            else:
                self.process_track_common(elem, track)

        if track.codec in FOURCCMap:
            track.codec = FOURCCMap[track.codec]
        elif '/' in track.codec and track.codec.split('/')[0] + '/' in FOURCCMap:
            track.codec = FOURCCMap[(track.codec.split('/')[0] + '/')]
        elif track.codec.startswith('A_'):
            track.codec = track.codec[2:]
        track.id = len(self.audio)
        self.audio.append(track)
        return track

    def process_chapters(self, chapters):
        elements = self.process_one_level(chapters)
        for elem in elements:
            if elem.get_id() == MATROSKA_EDITION_ENTRY_ID:
                buf = elem.get_data()
                index = 0
                while index < elem.get_len():
                    sub_elem = EbmlEntity(buf[index:])
                    if sub_elem.get_id() == MATROSKA_CHAPTER_ATOM_ID:
                        self.process_chapter_atom(sub_elem)
                    index += sub_elem.get_total_len() + sub_elem.get_crc_len()

    def process_chapter_atom(self, atom):
        elements = self.process_one_level(atom)
        chap = core.Chapter()
        for elem in elements:
            elem_id = elem.get_id()
            if elem_id == MATROSKA_CHAPTER_TIME_START_ID:
                chap.pos = elem.get_value() / 1000000 / 1000.0
            elif elem_id == MATROSKA_CHAPTER_FLAG_ENABLED_ID:
                chap.enabled = elem.get_value()
            elif elem_id == MATROSKA_CHAPTER_DISPLAY_ID:
                for display_elem in self.process_one_level(elem):
                    if display_elem.get_id() == MATROSKA_CHAPTER_STRING_ID:
                        chap.name = display_elem.get_utf8()

            elif elem_id == MATROSKA_CHAPTER_UID_ID:
                self.objects_by_uid[elem.get_value()] = chap

        log.debug('Chapter "%s" found', chap.name)
        chap.id = len(self.chapters)
        self.chapters.append(chap)

    def process_attachments(self, attachments):
        buf = attachments.get_data()
        index = 0
        while index < attachments.get_len():
            elem = EbmlEntity(buf[index:])
            if elem.get_id() == MATROSKA_ATTACHED_FILE_ID:
                self.process_attachment(elem)
            index += elem.get_total_len() + elem.get_crc_len()

    def process_attachment(self, attachment):
        elements = self.process_one_level(attachment)
        name = desc = mimetype = ''
        data = None
        for elem in elements:
            elem_id = elem.get_id()
            if elem_id == MATROSKA_FILE_NAME_ID:
                name = elem.get_utf8()
            elif elem_id == MATROSKA_FILE_DESC_ID:
                desc = elem.get_utf8()
            elif elem_id == MATROSKA_FILE_MIME_TYPE_ID:
                mimetype = elem.get_data()
            elif elem_id == MATROSKA_FILE_DATA_ID:
                data = elem.get_data()

        if mimetype.startswith('image/') and 'cover' in (name + desc).lower() and data:
            self.thumbnail = data
        log.debug('Attachment "%s" found' % name)
        return

    def process_tags(self, tags):
        for tag_elem in self.process_one_level(tags):
            tags_dict = core.Tags()
            targets = []
            for sub_elem in self.process_one_level(tag_elem):
                if sub_elem.get_id() == MATROSKA_SIMPLE_TAG_ID:
                    self.process_simple_tag(sub_elem, tags_dict)
                elif sub_elem.get_id() == MATROSKA_TARGETS_ID:
                    for target_elem in self.process_one_level(sub_elem):
                        target_elem_id = target_elem.get_id()
                        if target_elem_id in (MATRSOKA_TAGS_TRACK_UID_ID, MATRSOKA_TAGS_EDITION_UID_ID,
                         MATRSOKA_TAGS_CHAPTER_UID_ID, MATRSOKA_TAGS_ATTACHMENT_UID_ID):
                            targets.append(target_elem.get_value())
                        elif target_elem_id == MATROSKA_TARGET_TYPE_VALUE_ID:
                            continue

            if targets:
                for target in targets:
                    try:
                        self.objects_by_uid[target].tags.update(tags_dict)
                        self.tags_to_attributes(self.objects_by_uid[target], tags_dict)
                    except KeyError:
                        log.warning('Tags assigned to unknown/unsupported target uid %d', target)

            else:
                self.tags.update(tags_dict)
                self.tags_to_attributes(self, tags_dict)

    def process_simple_tag(self, simple_tag_elem, tags_dict):
        """
        Returns a dict representing the Tag element.
        """
        name = lang = value = children = None
        binary = False
        for elem in self.process_one_level(simple_tag_elem):
            elem_id = elem.get_id()
            if elem_id == MATROSKA_TAG_NAME_ID:
                name = elem.get_utf8().lower()
            elif elem_id == MATROSKA_TAG_STRING_ID:
                value = elem.get_utf8()
            elif elem_id == MATROSKA_TAG_BINARY_ID:
                value = elem.get_data()
                binary = True
            elif elem_id == MATROSKA_TAG_LANGUAGE_ID:
                lang = elem.get_utf8()
            elif elem_id == MATROSKA_SIMPLE_TAG_ID:
                if children is None:
                    children = core.Tags()
                self.process_simple_tag(elem, children)

        if children:
            children.value = value
            children.langcode = lang
            value = children
        else:
            if name.startswith('date_'):
                value = matroska_date_to_datetime(value)
            value = core.Tag(value, lang, binary)
        if name in tags_dict:
            if not isinstance(tags_dict[name], list):
                tags_dict[name] = [tags_dict[name]]
            tags_dict[name].append(value)
        else:
            tags_dict[name] = value
        return

    def tags_to_attributes(self, obj, tags):
        for name, tag in tags.items():
            if isinstance(tag, dict):
                self.tags_to_attributes(obj, tag)
                continue
            elif name not in TAGS_MAP:
                continue
            attr, filter = TAGS_MAP[name]
            if attr not in obj._keys and attr not in self._keys:
                continue
            value = [ item.value for item in tag ] if isinstance(tag, list) else tag.value
            if filter:
                try:
                    value = [ filter(item) for item in value ] if isinstance(value, list) else filter(value)
                except Exception as e:
                    log.warning('Failed to convert tag to core attribute: %s', e)

            if attr == 'trackno' and getattr(self, attr) is not None:
                self.season = self.trackno
                self.episode = value
                self.trackno = None
                continue
            if attr == 'title' and getattr(self, attr) is not None:
                self.series = self.title
            if attr in obj._keys:
                setattr(obj, attr, value)
            else:
                setattr(self, attr, value)

        return


Parser = Matroska