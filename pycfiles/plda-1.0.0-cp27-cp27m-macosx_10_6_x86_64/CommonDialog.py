# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\CommonDialog.py
# Compiled at: 2020-01-10 23:03:59
import wx, os

def MessageBox(parent, msg, title, button=wx.OK | wx.ICON_INFORMATION):
    dlg = wx.MessageDialog(parent, msg, title, button)
    val = dlg.ShowModal()
    dlg.Destroy()
    return val


def InputBox(parent=None, msg='', title=''):
    dlg = wx.TextEntryDialog(parent, msg, title, '')
    dlg.SetValue('')
    if dlg.ShowModal() == wx.ID_OK:
        return dlg.GetValue()
    dlg.Destroy()


def OpenFileDialog(parent, filter):
    tpath = os.getcwd()
    filters = ''
    for cmt, suffix in filter:
        filters += cmt + ' (*.' + suffix + ')|*.' + suffix
        filters += '|'

    filters = filters[:-1]
    dlg = wx.FileDialog(parent, message='Choose a file', defaultDir=os.getcwd(), defaultFile='', wildcard=filters, style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
    if dlg.ShowModal() == wx.ID_OK:
        paths = dlg.GetPaths()
        dlg.Destroy()
        os.chdir(tpath)
        return paths
    dlg.Destroy()


wildcard = 'Python source (*.py)|*.py|Compiled Python (*.pyc)|*.pyc|SPAM files (*.spam)|*.spam|Egg file (*.egg)|*.egg|All files (*.*)|*.*'