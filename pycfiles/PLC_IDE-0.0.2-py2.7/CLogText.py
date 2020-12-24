# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\IDE\CLogText.py
# Compiled at: 2020-01-19 10:17:02
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wx
logtext = None

def create_log(parent):
    global logtext
    logtext = wx.TextCtrl(parent, -1, '', size=(200, 100), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_READONLY)
    logtext.SetInsertionPoint(0)


def LogText(txt):
    logtext.write(txt + '\n')


def write(txt):
    logtext.write(txt + '\n')