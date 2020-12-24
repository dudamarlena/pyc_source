# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/dal/dal_main.py
# Compiled at: 2016-06-22 17:23:26
"""
处理main_view的数据

control和view中间层, 负责生成显示的内容(增加主题色彩)

    dal = MainDal(data)

    dal.title
    dal.love
    dal.prefix_selected
    dal.prefix_deselected
    dal.suffix_selected
    dal.suffix_deselected
    dal.lines
"""
import logging
from doubanfm.colorset.colors import on_light_red, color_func
logger = logging.getLogger('doubanfm')
RATE = [ '★' * i for i in range(1, 6) ]
PRO = on_light_red(' PRO ')
LOVE = ' ❤  '
PREFIX_SELECTED = '  > '
PREFIX_DESELECTED = '    '
SUFFIX_SELECTED = ''
SUFFXI_DESELECTED = ''

class MainDal(object):

    def __init__(self, data):
        self.c = data.theme
        self.data = data
        playingsong = data.playingsong if data.playingsong else {}
        self.song_total_time = playingsong.get('length', '0')
        self.song_kbps = playingsong.get('kbps', '0') + 'kbps'
        self.song_pro = '' if playingsong.get('kbps', '0') == '128' else PRO
        self.song_title = playingsong.get('title', '')
        self.song_albumtitle = playingsong.get('albumtitle', '')
        self.song_artist = playingsong.get('artist', '')
        self.song_like = data.song_like
        self.netease = data.netease
        self.volume = data.volume
        self.loop = data.loop
        self.pause = data.pause
        self.time = data.time
        self.user_name = data.user_name

    def set_time(self, time):
        u"""
        时间状态
        """
        rest_time = int(self.song_total_time) - self.time - 1
        minute = int(rest_time) / 60
        sec = int(rest_time) % 60
        return str(minute).zfill(2) + ':' + str(sec).zfill(2)

    @property
    def title(self):
        time = self.set_time(self.time)
        volume = str(self.volume) + '%' if self.volume != 0 else color_func(self.c['TITLE']['state'])('✖')
        if self.pause:
            loop = 'P'
        elif self.loop:
            loop = '⟲'
        else:
            loop = '→'
        source = '网易' if self.netease else ''
        title = [
         PREFIX_DESELECTED,
         color_func(self.c['TITLE']['doubanfm'])('DoubanFM'),
         '\\',
         color_func(self.c['TITLE']['username'])(self.user_name),
         '>>',
         color_func(self.c['PLAYINGSONG']['like'])(source),
         color_func(self.c['TITLE']['kbps'])(self.song_kbps),
         color_func(self.c['TITLE']['time'])(time),
         color_func(self.c['TITLE']['vol'])(volume),
         color_func(self.c['TITLE']['state'])(loop)]
        return (' ').join(title)

    @property
    def love(self):
        if self.song_like:
            return color_func(self.c['PLAYINGSONG']['like'])(LOVE)
        else:
            return ''

    @property
    def prefix_selected(self):
        return color_func(self.c['LINE']['arrow'])(PREFIX_SELECTED)

    @property
    def prefix_deselected(self):
        return PREFIX_DESELECTED

    @property
    def suffix_selected(self):
        love = self.love
        title = color_func(self.c['PLAYINGSONG']['title'])(self.song_title)
        albumtitle = color_func(self.c['PLAYINGSONG']['albumtitle'])(self.song_albumtitle)
        artist = color_func(self.c['PLAYINGSONG']['artist'])(self.song_artist)
        return (love + title + ' • ' + albumtitle + ' • ' + artist + ' ').replace('\\', '')

    @property
    def suffix_deselected(self):
        return SUFFXI_DESELECTED

    @property
    def lines(self):
        return self.data.lines