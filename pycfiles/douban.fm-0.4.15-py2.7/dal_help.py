# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/dal/dal_help.py
# Compiled at: 2016-06-22 17:23:26
from doubanfm.dal.dal_main import MainDal
from doubanfm.colorset.colors import color_func

class HelpDal(MainDal):

    def __init__(self, data):
        super(HelpDal, self).__init__(data)
        self.keys = data.keys

    @property
    def lines(self):
        keys = self.keys
        lines = []
        lines.append('     ' + color_func(self.c['PLAYINGSONG']['title'])('移动') + '                 ' + color_func(self.c['PLAYINGSONG']['title'])('音乐') + '\r')
        lines.append('     ' + '[%(DOWN)s] ---> 下          [space] ---> 播放' % keys + '\r')
        lines.append('     ' + '[%(UP)s] ---> 上          [%(OPENURL)s] ---> 打开歌曲主页' % keys + '\r')
        lines.append('     ' + '[%(TOP)s] ---> 移到最顶    [%(NEXT)s] ---> 下一首' % keys + '\r')
        lines.append('     ' + '[%(BOTTOM)s] ---> 移到最底    [%(RATE)s] ---> 喜欢/取消喜欢' % keys + '\r')
        lines.append(' ' * 26 + '[%(BYE)s] ---> 不再播放' % keys + '\r')
        lines.append('     ' + color_func(self.c['PLAYINGSONG']['title'])('音量') + '                 ' + '[%(PAUSE)s] ---> 暂停' % keys + '\r')
        lines.append('     ' + '[=] ---> 增          [%(QUIT)s] ---> 退出' % keys + '\r')
        lines.append('     ' + '[-] ---> 减          [%(LOOP)s] ---> 单曲循环' % keys + '\r')
        lines.append('     ' + '[%(MUTE)s] ---> 静音        [i] ---> 网易320k音乐' % keys + '\r')
        lines.append('')
        lines.append('     ' + color_func(self.c['PLAYINGSONG']['title'])('歌词') + '\r')
        lines.append('     ' + '[%(LRC)s] ---> 歌词' % keys + '\r')
        return lines