# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/_audiodata.py
# Compiled at: 2007-11-27 08:43:15
try:
    from zope.app.annotation import interfaces as annointerfaces
except ImportError, err:
    from zope.annotation import interfaces as annointerfaces

from zope import interface
from p4a.audio import interfaces
from p4a.audio.ogg.thirdparty.mutagen.oggvorbis import Open as openaudio

def _safe(v):
    if isinstance(v, list) or isinstance(v, tuple):
        if len(v) >= 1:
            return v[0]
        else:
            return
    return v


class OggAudioDataAccessor(object):
    """An AudioDataAccessor for ogg"""
    __module__ = __name__
    interface.implements(interfaces.IAudioDataAccessor)

    def __init__(self, context):
        self._filecontent = context

    @property
    def audio_type(self):
        return 'Ogg Vorbis'

    @property
    def _audio(self):
        return interfaces.IAudio(self._filecontent)

    @property
    def _audio_data(self):
        annotations = annointerfaces.IAnnotations(self._filecontent)
        return annotations.get(self._audio.ANNO_KEY, None)

    def load(self, filename):
        oggfile = openaudio(filename)
        self._audio_data['title'] = _safe(oggfile.get('title', ''))
        self._audio_data['artist'] = _safe(oggfile.get('artist', ''))
        self._audio_data['album'] = _safe(oggfile.get('album', ''))
        self._audio_data['year'] = _safe(oggfile.get('date', ''))
        self._audio_data['idtrack'] = _safe(oggfile.get('tracknumber', ''))
        self._audio_data['genre'] = _safe(oggfile.get('genre', ''))
        self._audio_data['comment'] = _safe(oggfile.get('description', ''))
        self._audio_data['bit_rate'] = long(oggfile.info.bitrate)
        self._audio_data['length'] = long(oggfile.info.length)
        self._audio_data['frequency'] = long(oggfile.info.sample_rate)

    def store(self, filename):
        oggfile = openaudio(filename)
        oggfile['title'] = self._audio.title or ''
        oggfile['artist'] = self._audio.artist or ''
        oggfile['album'] = self._audio.album or ''
        oggfile['date'] = self._audio.year or ''
        oggfile['tracknumber'] = self._audio.idtrack or ''
        oggfile.save()