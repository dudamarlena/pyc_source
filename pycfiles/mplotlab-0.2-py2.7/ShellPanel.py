# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\ShellPanel.py
# Compiled at: 2016-02-07 09:44:32
from wx.py.shell import Shell
from mplotlab import App

class ShellPanel(Shell):

    def __init__(self, parent):
        Shell.__init__(self, parent, introText='')

    def refreshLocals(self, **dlocals):
        dlocals['app'] = App()
        dlocals['win'] = App().GetTopWindow()
        self.interp.locals.update(dlocals)