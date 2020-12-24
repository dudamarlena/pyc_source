# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/views/manager_view.py
# Compiled at: 2016-06-22 17:23:26
from doubanfm.views.lrc_view import Lrc
from doubanfm.dal.dal_manager import ManagerDal

class Manager(Lrc):
    """帮助界面"""

    def __init__(self, data):
        super(Manager, self).__init__(data)

    def set_dal(self):
        dal = ManagerDal(self.data)
        self.c = dal.c
        self.set_title(dal.title)

    def display(self):
        self.set_dal()
        self.make_display_lines()
        for i in self.display_lines:
            print i

    def make_display_lines(self):
        self.screen_height, self.screen_width = self.linesnum()
        display_lines = [
         '']
        display_lines.append(self._title + '\r')
        display_lines.append('')
        self.display_lines = display_lines