# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\template_cli\template_cli\Styles\CommonHelper.py
# Compiled at: 2019-04-15 07:08:15
# Size of source mod 2**32: 991 bytes
"""
读取CSS用模块。
"""
from .CustomTitlebar.framelesswindow import FramelessWindow
import sys, os
from linecache import getline

class CommonHelper:

    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as (f):
            border_color = getline(style, 2).split(':')[(-1)].strip()[:-1]
            os.environ['border_color'] = border_color
            return f.read()

    @staticmethod
    def FrameCustomerTitle(ui, title='python', setparent=False, icon=''):
        framelessWindow = FramelessWindow(title, icon=icon)
        styleFile = os.path.join(os.path.dirname(sys.argv[0]), 'Styles/style.css')
        qssStyle = CommonHelper.readQss(styleFile)
        framelessWindow.setStyleSheet(qssStyle)
        framelessWindow.setContent(ui)
        if setparent:
            ui.setParent(framelessWindow)
        return framelessWindow