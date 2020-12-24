# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/model.py
# Compiled at: 2016-06-22 17:23:26
"""
数据层
"""
from threading import RLock, Thread
import logging, functools, Queue
from doubanfm.API.api import Doubanfm
from doubanfm.API.netease_api import Netease
from doubanfm.config import db_config
logger = logging.getLogger('doubanfm')
douban = Doubanfm()
mutex = RLock()
QUEUE_SIZE = 5

class Playlist(object):
    """
    播放列表, 各个方法互斥

    使用方法:

        playlist = Playlist()

        playingsong = playlist.get_song()

        获取当前播放歌曲
        playingsong = playlist.get_playingsong()
    """

    def __init__(self):
        self._playlist = Queue.Queue(QUEUE_SIZE)
        self._daily_playlist = []
        self._daily_playlist_index = -1
        self._playingsong = None
        self._get_first_song()
        self._lrc = {}
        self._pre_playingsong = None
        self.hash_sid = {}
        return

    def lock(func):
        u"""
        互斥锁
        """

        @functools.wraps(func)
        def _func(*args, **kwargs):
            mutex.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                mutex.release()

        return _func

    def _watchdog(self):
        u"""
        更新队列线程
        """
        sid = self._playingsong['sid']
        while 1:
            while 1:
                song = douban.get_song(sid)
                sid = song['sid']
                if sid not in self.hash_sid:
                    break

            self._playlist.put(song)
            if not self._playingsong:
                self._playlist.get(False)

    @lock
    def _get_first_song(self):
        song = douban.get_first_song()
        self._playlist.put(song)
        self._playingsong = song
        Thread(target=self._watchdog).start()

    def get_lrc(self):
        u"""
        返回当前播放歌曲歌词
        """
        if self._playingsong != self._pre_playingsong:
            self._lrc = douban.get_lrc(self._playingsong)
            self._pre_playingsong = self._playingsong
        return self._lrc

    def set_channel(self, channel_num):
        u"""
        设置api发送的FM频道

        :params channel_num: channel_list的索引值 int
        """
        douban.set_channel(channel_num)
        self.empty()
        if channel_num != 2:
            self._get_first_song()

    def set_song_like(self, playingsong):
        douban.rate_music(playingsong['sid'])

    def set_song_unlike(self, playingsong):
        douban.unrate_music(playingsong['sid'])

    def get_daily_songs(self):
        u"""
        获取每日推荐歌曲
        """
        self._daily_playlist = douban.get_daily_songs()
        for index, i in enumerate(self._daily_playlist):
            i['title'] = str(index + 1) + '/' + str(len(self._daily_playlist)) + ' ' + i['title']

    def get_daily_song(self, netease=False):
        u"""
        获取单个歌曲
        """
        if not self._daily_playlist:
            self.get_daily_songs()
            self._daily_playlist_index = 0
        else:
            self._daily_playlist_index = (self._daily_playlist_index + 1) % len(self._daily_playlist)
        song = self._daily_playlist[self._daily_playlist_index]
        song['index'] = self._daily_playlist_index
        self.get_netease_song(song, netease)
        self._playingsong = song
        return song

    @lock
    def bye(self):
        u"""
        不再播放, 返回新列表
        """
        douban.bye(self._playingsong['sid'])

    @lock
    def get_song(self, netease=False):
        u"""
        获取歌曲, 对外统一接口
        """
        song = self._playlist.get(True)
        self.hash_sid[song['sid']] = True
        self.get_netease_song(song, netease)
        self._playingsong = song
        return song

    def get_netease_song(self, song, netease):
        if netease:
            url, kbps = Netease().get_url_and_bitrate(song['title'])
            if url and kbps:
                song['url'], song['kbps'] = url, kbps

    @lock
    def get_playingsong(self):
        return self._playingsong

    @lock
    def empty(self):
        u"""
        清空playlist
        """
        self._playingsong = None
        self._playlist = Queue.Queue(QUEUE_SIZE)
        return

    def submit_music(self, playingsong):
        douban.submit_music(playingsong['sid'])


class History(object):

    def __init__(self):
        db_config.history


class Channel(object):

    def __init__(self):
        self.lines = douban.channels