# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/disc/audio.py
# Compiled at: 2008-10-19 10:01:09
__all__ = [
 'Parser']
import logging, kaa.metadata
from kaa.metadata.audio.core import Music as AudioTrack
import core, cdrom, CDDB
log = logging.getLogger('metadata')

class AudioDisc(core.Disc):
    """
    Audio CD support. It provides a list of tracks and if on Internet
    connection is available it will use CDDB for the metadata.
    """

    def __init__(self, device):
        core.Disc.__init__(self)
        self.offset = 0
        if self.is_disc(device) != 1:
            raise core.ParseError()
        self.query(device)
        self.mime = 'audio/cd'
        self.type = 'CD'
        self.subtype = 'audio'

    def query(self, device):
        cdromfd = cdrom.audiocd_open(device)
        disc_id = cdrom.audiocd_id(cdromfd)
        if kaa.metadata.USE_NETWORK:
            try:
                query_stat, query_info = CDDB.query(disc_id)
            except Exception as e:
                query_stat = 404

        else:
            query_stat = 404
        if query_stat == 210 or query_stat == 211:
            query_stat = 200
            for i in query_info:
                if i['title'] != i['title'].upper():
                    query_info = i
                    break
            else:
                query_info = query_info[0]

        else:
            if query_stat != 200:
                log.error('failure getting disc info, status %i' % query_stat)
            if query_stat == 200:
                qi = query_info['title'].split('/')
                self.artist = qi[0].strip()
                self.title = qi[1].strip()
                for type in ('title', 'artist'):
                    if getattr(self, type) and getattr(self, type)[0] in ('"', "'") and getattr(self, type)[(-1)] in ('"',
                                                                                                                      "'"):
                        setattr(self, type, getattr(self, type)[1:-1])

                read_stat, read_info = CDDB.read(query_info['category'], query_info['disc_id'])
                if read_stat == 210:
                    self.year = read_info['DYEAR']
                    for i in range(0, disc_id[1]):
                        mi = AudioTrack()
                        mi.title = read_info[('TTITLE' + `i`)]
                        mi.album = self.title
                        mi.artist = self.artist
                        mi.genre = query_info['category']
                        mi.year = self.year
                        mi.codec = 'PCM'
                        mi.samplerate = 44100
                        mi.trackno = i + 1
                        mi.trackof = disc_id[1]
                        self.tracks.append(mi)
                        for type in ('title', 'album', 'artist', 'genre'):
                            if getattr(mi, type) and getattr(mi, type)[0] in ('"',
                                                                              "'") and getattr(mi, type)[(-1)] in ('"',
                                                                                                                   "'"):
                                setattr(mi, type, getattr(mi, type)[1:-1])

                else:
                    log.error('failure getting track info, status: %i' % read_stat)
                    query_stat = 400
            if query_stat != 200:
                log.error('failure getting disc info, status %i' % query_stat)
                self.no_caching = 1
                for i in range(0, disc_id[1]):
                    mi = AudioTrack()
                    mi.title = 'Track %s' % (i + 1)
                    mi.codec = 'PCM'
                    mi.samplerate = 44100
                    mi.trackno = i + 1
                    mi.trackof = disc_id[1]
                    self.tracks.append(mi)

            first, last = cdrom.audiocd_toc_header(cdromfd)
            lmin = 0
            lsec = 0
            num = 0
            for i in range(first, last + 2):
                if i == last + 1:
                    min, sec, frames = cdrom.audiocd_leadout(cdromfd)
                else:
                    min, sec, frames = cdrom.audiocd_toc_entry(cdromfd, i)
                if num:
                    self.tracks[(num - 1)].length = (min - lmin) * 60 + (sec - lsec)
                num += 1
                lmin, lsec = min, sec

        for t in self.tracks:
            if not self.artist or not t.title.startswith(self.artist):
                break
        else:
            for t in self.tracks:
                t.title = t.title[len(self.artist):].lstrip('/ \t-_')

            for t in self.tracks:
                if not self.title or not t.title.startswith(self.title):
                    break
            else:
                for t in self.tracks:
                    t.title = t.title[len(self.title):].lstrip('/ \t-_')

                cdromfd.close()


Parser = AudioDisc