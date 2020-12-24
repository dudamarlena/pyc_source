# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/views/base_view.py
# Compiled at: 2016-06-22 17:23:26
"""
用print设计的滚动终端界面

_prefix_selected:可以指定当前指向行的前缀
_prefix_deselected:暂时没有用,如果想保持选项行一致需要填写和PREFIX_SELECTED一样大小的空格
_suffix_selected:对选中行进行标记
_suffix_deselected:暂时无用
_title:界面标题的设定
"""
import sys
sys.stdout.write('\x1b[?25l')

class Cli(object):

    def __init__(self):
        self.markline = 0
        self.topline = 0
        self.displayline = 0
        self.display_lines = []
        self._title = ''
        self._love = ''
        self._prefix_selected = ''
        self._prefix_deselected = ''
        self._suffix_selected = ''
        self._suffix_deselected = ''
        self.screen_height, self.screen_width = self.linesnum()

    def set_title(self, string):
        self._title = string

    def set_love(self, string):
        self._love = string

    def set_prefix_selected(self, string):
        self._prefix_selected = string

    def set_prefix_deselected(self, string):
        self._prefix_deselected = string

    def set_suffix_selected(self, string):
        self._suffix_selected = string

    def set_suffix_deselected(self, string):
        self._suffix_deselected = string

    def set_lines(self, string):
        self._lines = string

    def set_sort_lrc_dict(self, string):
        self._sort_lrc_dict = string

    def set_displayline(self):
        u"""
        显示歌曲信息的行号
        """
        self.displayline = self.markline + self.topline

    def set_channel(self):
        self.set_displayline()
        return self.displayline

    def linesnum(self):
        u"""
        测试屏幕显示行数, 每行字符数

        return: 屏幕高度 int
                屏幕宽度 int
        """
        import os
        env = os.environ

        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            except:
                return

            return cr

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass

        if not cr:
            cr = (
             env.get('LINES', 25), env.get('COLUMNS', 80))
        return (
         int(cr[0]), int(cr[1]))

    def make_display_lines(self):
        u"""
        生成输出信息
        """
        pass

    def display(self):
        u"""
        显示输出信息
        """
        pass

    def updown(self, increment):
        u"""
        屏幕上下滚动

        :params incrment: 1 向下滚动
                          -1 向上滚动
        """
        scroll_line_num = self.screen_height - 4
        if increment == -1 and self.markline == 0 and self.topline != 0:
            self.topline -= 1
        elif increment == 1 and self.markline + self.topline != len(self._lines) - 1 and self.markline == scroll_line_num:
            self.topline += 1
        if increment == -1 and self.markline != 0:
            self.markline -= 1
        elif increment == 1 and self.markline != scroll_line_num and self.markline < len(self._lines) - 1:
            self.markline += 1

    def up(self):
        self.updown(-1)

    def down(self):
        self.updown(1)

    def go_bottom(self):
        if len(self._lines) < self.screen_height - 3:
            self.markline = len(self._lines) - 1
        else:
            self.markline = self.screen_height - 4
            self.topline = len(self._lines) - self.screen_height + 3

    def go_top(self):
        self.markline = 0
        self.topline = 0

    def is_cn_char(self, i):
        u"""
        判断是否为中文字符(歌词居中使用)
        : TODO 日语好像会有bug
        """
        return 19968 <= ord(i) < 40870

    def center_num(self, string):
        u"""
        返回总字符数(考虑英文和中文在终端所占字块)

        return: int
        """
        l = 0
        for i in string:
            l += 2 if self.is_cn_char(i) else 1

        return l