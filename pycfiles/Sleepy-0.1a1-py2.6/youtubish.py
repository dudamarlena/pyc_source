# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/youtubish.py
# Compiled at: 2011-03-22 16:30:41
from gdata.youtube.service import YouTubeService
from sleepy.shorties import Ago, s, Duration, date_parse
from sleepy.lonsies import Entries

class Video(object):

    def __init__(self, entry, user=None, use_cache=True):
        self.title = entry.media.title.text
        self.description = entry.media.description.text
        self.duration = Duration(entry.media.duration.seconds)
        self.published = date_parse(entry.published.text)
        self.updated = date_parse(entry.updated.text)
        self.watch_url = entry.media.player.url
        self.flash_url = entry.GetSwfUrl()
        self.thumbnail = entry.media.thumbnail[3].url

    @property
    def ago(self):
        return Ago(self.published)


def uri(user):
    return s('http://gdata.youtube.com/feeds/api/users/{{ user }}/uploads', user=user)


def service():
    return YouTubeService()


videos = Entries(entry_class=Video, user_config_key='youtube_user', createfunc=lambda user: service().GetYouTubeVideoFeed(uri(user)).entry, cache_name='youtube_feed')