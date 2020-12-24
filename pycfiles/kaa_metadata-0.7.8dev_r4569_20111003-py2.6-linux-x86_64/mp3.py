# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/mp3.py
# Compiled at: 2010-06-20 17:22:01
__all__ = [
 'Parser']
import re, sys, logging, struct
from kaa.strutils import str_to_unicode
import core, ID3
from eyeD3 import tag as eyeD3_tag
from eyeD3 import frames as eyeD3_frames
log = logging.getLogger('metadata')
MP3_INFO_TABLE = {'LINK': 'link', 'TALB': 'album', 
   'TCOM': 'composer', 
   'TCOP': 'copyright', 
   'TDOR': 'release', 
   'TYER': 'userdate', 
   'TEXT': 'text', 
   'TIT2': 'title', 
   'TLAN': 'language', 
   'TLEN': 'length', 
   'TMED': 'media_type', 
   'TPE1': 'artist', 
   'TPE2': 'artist', 
   'TRCK': 'trackno', 
   'TPOS': 'discs', 
   'TPUB': 'publisher'}
_bitrates = [
 [
  [
   0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256, None],
  [
   0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, None],
  [
   0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, None]],
 [
  [
   0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, None],
  [
   0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, None],
  [
   0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, None]]]
_samplerates = [
 [
  11025, 12000, 8000, None],
 [
  None, None, None, None],
 [
  22050, 24000, 16000, None],
 [
  44100, 48000, 32000, None]]
_modes = [
 'stereo', 'joint stereo', 'dual channel', 'mono']
_MP3_HEADER_SEEK_LIMIT = 4096

class MP3(core.Music):
    fileName = str()
    fileSize = int()

    def __init__(self, file, tagVersion=eyeD3_tag.ID3_ANY_VERSION):
        core.Music.__init__(self)
        self.fileName = file.name
        self.codec = 85
        self.mime = 'audio/mpeg'
        id3 = None
        try:
            id3 = eyeD3_tag.Mp3AudioFile(file.name)
        except eyeD3_tag.InvalidAudioFormatException:
            raise core.ParseError()
        except eyeD3_tag.TagException:
            if log.level < 30:
                log.exception('mp3 tag parsing %s failed!' % file.name)
        except Exception:
            if log.level < 30:
                log.exception('mp3 tag parsing %s failed!' % file.name)

        if not id3:
            s = file.read(4096)
            if not s[:3] == 'ID3':
                if not re.compile('0*\\xFF\\xFB\\xB0\\x04$').search(s):
                    if not re.compile('0*\\xFF\\xFA\\xB0\\x04$').search(s):
                        raise core.ParseError()
        try:
            if id3 and id3.tag:
                log.debug(id3.tag.frames)
                for frame in id3.tag.frames['COMM']:
                    if 'created by grip' not in frame.comment.lower():
                        continue
                    for frame in id3.tag.frames:
                        if hasattr(frame, 'text') and isinstance(frame.text, unicode):
                            try:
                                frame.text = frame.text.encode('latin-1').decode('utf-8')
                            except UnicodeError:
                                pass

                for k, var in MP3_INFO_TABLE.items():
                    if id3.tag.frames[k]:
                        self._set(var, id3.tag.frames[k][0].text)

                if id3.tag.frames['APIC']:
                    pic = id3.tag.frames['APIC'][0]
                    if pic.imageData:
                        self.thumbnail = pic.imageData
                if id3.tag.getYear():
                    self.userdate = id3.tag.getYear()
                tab = {}
                for f in id3.tag.frames:
                    if f.__class__ is eyeD3_frames.TextFrame:
                        tab[f.header.id] = f.text
                    elif f.__class__ is eyeD3_frames.UserTextFrame:
                        self._set('_' + f.description, f.text)
                        tab['_' + f.description] = f.text
                    elif f.__class__ is eyeD3_frames.DateFrame:
                        tab[f.header.id] = f.date_str
                    elif f.__class__ is eyeD3_frames.CommentFrame:
                        tab[f.header.id] = f.comment
                        self.comment = str_to_unicode(f.comment)
                    elif f.__class__ is eyeD3_frames.URLFrame:
                        tab[f.header.id] = f.url
                    elif f.__class__ is eyeD3_frames.UserURLFrame:
                        tab[f.header.id] = f.url
                    elif f.__class__ is eyeD3_frames.ImageFrame:
                        tab[f.header.id] = f
                    else:
                        log.debug(f.__class__)

                self._appendtable('id3v2', tab)
                if id3.tag.frames['TCON']:
                    genre = None
                    tcon = id3.tag.frames['TCON'][0].text
                    try:
                        genre = int(tcon)
                    except ValueError:
                        try:
                            genre = int(tcon[1:tcon.find(')')])
                        except ValueError:
                            self.genre = str_to_unicode(tcon)

                    if genre is not None:
                        try:
                            self.genre = ID3.GENRE_LIST[genre]
                        except KeyError:
                            self.genre = 'Unknown'

                if not self.trackof and self.trackno and self.trackno.find('/') > 0:
                    self.trackof = self.trackno[self.trackno.find('/') + 1:]
                    self.trackno = self.trackno[:self.trackno.find('/')]
            if id3:
                self.length = id3.getPlayTime()
        except Exception:
            if log.level < 30:
                log.exception('parse error')

        offset, header = self._find_header(file)
        if offset == -1 or header is None:
            return
        else:
            self._parse_header(header)
            if id3:
                vbr, self.bitrate = id3.getBitRate()
            return

    def _find_header(self, file):
        file.seek(0, 0)
        amount_read = 0
        amt = 4
        while amount_read < _MP3_HEADER_SEEK_LIMIT:
            header = file.read(amt)
            if len(header) < amt:
                return (-1, None)
            amount_read = amount_read + len(header)
            amt = 500
            offset = header.find(chr(255))
            if offset == -1:
                continue
            if offset + 4 > len(header):
                more = file.read(4)
                if len(more) < 4:
                    return (-1, None)
                amount_read = amount_read + 4
                header = header + more
            if ord(header[(offset + 1)]) >> 5 != 7:
                continue
            return (amount_read - len(header) + offset, header[offset:offset + 4])

        return (-1, None)

    def _parse_header(self, header):
        bytes = struct.unpack('>i', header)[0]
        mpeg_version = bytes >> 19 & 3
        layer = bytes >> 17 & 3
        bitrate = bytes >> 12 & 15
        samplerate = bytes >> 10 & 3
        mode = bytes >> 6 & 3
        if mpeg_version == 0:
            self.version = 2.5
        elif mpeg_version == 2:
            self.version = 2
        elif mpeg_version == 3:
            self.version = 1
        else:
            return
        if layer > 0:
            layer = 4 - layer
        else:
            return
        self.bitrate = _bitrates[(mpeg_version & 1)][(layer - 1)][bitrate]
        self.samplerate = _samplerates[mpeg_version][samplerate]
        if self.bitrate is None or self.samplerate is None:
            return
        else:
            self._set('mode', _modes[mode])
            return


Parser = MP3