# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/views/main_view.py
# Compiled at: 2016-06-22 17:23:26
from threading import RLock
from doubanfm.colorset.colors import color_func
from doubanfm.dal.dal_main import MainDal
from doubanfm.views.base_view import Cli
mutex = RLock()

class Win(Cli):
    """窗体"""

    def __init__(self, data):
        super(Win, self).__init__()
        self.data = data
        self.displayline = data.channel
        self.display_lines = ''
        self.disable = False
        self.override = False
        self.info = None
        return

    def set_dal(self):
        dal = MainDal(self.data)
        self.c = dal.c
        self.set_title(dal.title)
        self.set_love(dal.love)
        self.set_prefix_selected(dal.prefix_selected)
        self.set_prefix_deselected(dal.prefix_deselected)
        if self.override:
            self.set_suffix_selected(self.info)
        else:
            self.set_suffix_selected(dal.suffix_selected)
        self.set_suffix_deselected(dal.suffix_deselected)
        self.set_lines(dal.lines)

    def override_suffix_selected(self, info):
        u"""
        设置显示信息
        """
        if info:
            self.override = True
            self.info = info

    def cancel_override(self):
        self.override = False
        self.info = None
        return

    def set_disable(self):
        self.disable = True

    def display(self):
        mutex.acquire()
        try:
            self.set_dal()
            self.make_display_lines()
            print ('\n').join(self.display_lines)
        finally:
            mutex.release()

    def make_display_lines(self):
        u"""
        生成输出行

        注意: 多线程终端同时输出会有bug, 导致起始位置偏移, 需要在每行加
        """
        self.screen_height, self.screen_width = self.linesnum()
        display_lines = [
         '\r']
        display_lines.append(self._title + '\r')
        top = self.topline
        bottom = self.topline + self.screen_height - 3
        for index, i in enumerate(self._lines[top:bottom]):
            if index == self.markline:
                prefix = self._prefix_selected
                i = color_func(self.c['LINE']['highlight'])(i)
            else:
                prefix = self._prefix_deselected
            if index + self.topline == self.displayline:
                suffix = self._suffix_selected
            else:
                suffix = self._suffix_deselected
            line = '%s %s %s' % (prefix, i, suffix)
            line = color_func(self.c['LINE']['line'])(line)
            display_lines.append(line + '\r')

        return_num = self.screen_height - 3 - len(self._lines)
        for _ in range(return_num):
            display_lines.append('\r')

        self.display_lines = display_lines