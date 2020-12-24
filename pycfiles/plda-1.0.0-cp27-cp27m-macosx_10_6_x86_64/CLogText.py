# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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