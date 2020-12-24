# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/core.py
# Compiled at: 2011-01-24 19:19:40
import re
from kaa.metadata.core import ParseError, Media, MEDIA_VIDEO, MEDIA_SUBTITLE, MEDIA_CHAPTER, MEDIA_AV, MEDIA_AUDIO, MEDIA_DISC, Collection, Tag, Tags, feature_enabled, feature_config
from kaa.metadata.audio.core import Audio as AudioStream
VIDEOCORE = [
 'length', 'encoder', 'bitrate', 'samplerate', 'codec', 'format',
 'samplebits', 'width', 'height', 'fps', 'aspect', 'trackno',
 'fourcc', 'id', 'enabled', 'default', 'codec_private']
AVCORE = [
 'length', 'encoder', 'trackno', 'trackof', 'copyright', 'product',
 'genre', 'writer', 'producer', 'studio', 'rating', 'actors', 'thumbnail',
 'delay', 'image', 'video', 'audio', 'subtitles', 'chapters', 'software',
 'summary', 'synopsis', 'season', 'episode', 'series']

class VideoStream(Media):
    """
    Video Tracks in a Multiplexed Container.
    """
    _keys = Media._keys + VIDEOCORE
    media = MEDIA_VIDEO


class Chapter(Media):
    """
    Chapter in a Multiplexed Container.
    """
    _keys = [
     'enabled', 'name', 'pos', 'id']
    media = MEDIA_CHAPTER

    def __init__(self, name=None, pos=0):
        Media.__init__(self)
        self.name = name
        self.pos = pos
        self.enabled = True


class Subtitle(Media):
    """
    Subtitle Tracks in a Multiplexed Container.
    """
    _keys = [
     'enabled', 'default', 'langcode', 'language', 'trackno', 'title',
     'id', 'codec']
    media = MEDIA_SUBTITLE

    def __init__(self, language=None):
        Media.__init__(self)
        self.language = language


class AVContainer(Media):
    """
    Container for Audio and Video streams. This is the Container Type for
    all media, that contain more than one stream.
    """
    _keys = Media._keys + AVCORE
    media = MEDIA_AV

    def __init__(self):
        Media.__init__(self)
        self.audio = []
        self.video = []
        self.subtitles = []
        self.chapters = []

    def _set_url(self, url):
        """
        Set the URL of the source
        """
        Media._set_url(self, url)
        if feature_enabled('VIDEO_SERIES_PARSER') and not self.series:
            match = re.split(feature_config('VIDEO_SERIES_PARSER'), url)
            if match and len(match) == 6:
                try:
                    self.season, self.episode = int(match[2]), int(match[3])
                    self.series, self.title = match[1], match[4]
                except ValueError:
                    pass

    def _finalize(self):
        """
        Correct same data based on specific rules
        """
        Media._finalize(self)
        if not self.length and len(self.video) and self.video[0].length:
            self.length = 0
            for track in self.video + self.audio:
                if track.length:
                    self.length = max(self.length, track.length)