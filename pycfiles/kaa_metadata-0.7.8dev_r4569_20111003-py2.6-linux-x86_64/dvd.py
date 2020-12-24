# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/disc/dvd.py
# Compiled at: 2008-10-19 10:01:09
__all__ = [
 'Parser']
import os, logging, glob, kaa.metadata.video.core as video, kaa.metadata.audio.core as audio, core
try:
    import _ifoparser
except ImportError:
    _ifoparser = None

log = logging.getLogger('metadata')
_video_height = (480, 576, 0, 576)
_video_width = (720, 704, 352, 352)
_video_fps = (0, 25.0, 0, 29.97)
_video_format = ('NTSC', 'PAL')
_video_aspect = (4.0 / 3, 16.0 / 9, 1.0, 16.0 / 9)

class DVDVideo(video.VideoStream):

    def __init__(self, data):
        video.VideoStream.__init__(self)
        self.length = data[0]
        self.fps = _video_fps[data[1]]
        self.format = _video_format[data[2]]
        self.aspect = _video_aspect[data[3]]
        self.width = _video_width[data[4]]
        self.height = _video_height[data[5]]
        self.codec = 'MP2V'


class DVDAudio(audio.Audio):
    _keys = audio.Audio._keys

    def __init__(self, info):
        audio.Audio.__init__(self)
        self.id, self.language, self.codec, self.channels, self.samplerate = info


class DVDTitle(video.AVContainer):
    _keys = video.AVContainer._keys + ['angles']

    def __init__(self, info):
        video.AVContainer.__init__(self)
        self.chapters = []
        pos = 0
        for length in info[0]:
            chapter = video.Chapter()
            chapter.pos = pos
            pos += length
            self.chapters.append(chapter)

        self.angles = info[1]
        self.mime = 'video/mpeg'
        self.video.append(DVDVideo(info[2:8]))
        self.length = self.video[0].length
        for a in info[(-2)]:
            self.audio.append(DVDAudio(a))

        for id, lang in info[(-1)]:
            sub = video.Subtitle(lang)
            sub.id = id
            self.subtitles.append(sub)


class DVDInfo(core.Disc):
    """
    DVD parser for DVD discs, DVD iso files and hard-disc and DVD
    directory structures with a VIDEO_TS folder.
    """
    _keys = core.Disc._keys + ['length']

    def __init__(self, device):
        core.Disc.__init__(self)
        self.offset = 0
        if isinstance(device, file):
            self.parseDVDiso(device)
        else:
            if os.path.isdir(device):
                self.parseDVDdir(device)
            else:
                self.parseDisc(device)
            self.length = 0
            first = 0
            for t in self.tracks:
                self.length += t.length
                if not first:
                    first = t.length

        if self.length / len(self.tracks) == first:
            self.length = first
        self.mime = 'video/dvd'
        self.type = 'DVD'
        self.subtype = 'video'

    def _parse(self, device):
        if not _ifoparser:
            log.debug('kaa.metadata not compiled with DVD support')
            raise core.ParseError()
        info = _ifoparser.parse(device)
        if not info:
            raise core.ParseError()
        for pos, title in enumerate(info):
            ti = DVDTitle(title)
            ti.trackno = pos + 1
            ti.trackof = len(info)
            self.tracks.append(ti)

    def parseDVDdir(self, dirname):

        def iglob(path, ifile):
            file_glob = ('').join([ '[%s%s]' % (c, c.upper()) for c in ifile ])
            return glob.glob(os.path.join(path, file_glob))

        if True not in [ os.path.isdir(x) for x in iglob(dirname, 'video_ts') ] + [ os.path.isfile(x) for x in iglob(dirname, 'video_ts.vob') ]:
            raise core.ParseError()
        self._parse(dirname)
        return 1

    def parseDisc(self, device):
        if self.is_disc(device) != 2:
            raise core.ParseError()
        f = open(device, 'rb')
        f.seek(32768, 0)
        buffer = f.read(60000)
        if buffer.find('UDF') == -1:
            f.close()
            raise core.ParseError()
        buffer += f.read(550000)
        f.close()
        if buffer.find('VIDEO_TS') == -1 and buffer.find('VIDEO_TS.IFO') == -1 and buffer.find('OSTA UDF Compliant') == -1:
            raise core.ParseError()
        self._parse(device)

    def parseDVDiso(self, f):
        f.seek(32768, 0)
        buffer = f.read(60000)
        if buffer.find('UDF') == -1:
            raise core.ParseError()
        buffer += f.read(550000)
        if buffer.find('VIDEO_TS') == -1 and buffer.find('VIDEO_TS.IFO') == -1 and buffer.find('OSTA UDF Compliant') == -1:
            raise core.ParseError()
        self._parse(f.name)


Parser = DVDInfo