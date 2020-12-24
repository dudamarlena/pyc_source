# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/mac_text_fixer.py
# Compiled at: 2013-09-24 00:46:30
import wx

def fix_text_sizes(parent):
    fix_text_sizes_recur(parent)
    parent.Fit()


def fix_text_sizes_recur(control):
    """Recursively travels window hierarchy fixing text controls."""
    font_size = control.GetFont().GetPointSize()
    if font_size == 10:
        new_font_size = font_size + 1
    else:
        new_font_size = max(10, font_size)
    if font_size != new_font_size:
        old_font = control.GetFont()
        new_font = wx.Font(pointSize=old_font.GetPointSize(), family=old_font.GetFamily(), style=old_font.GetStyle(), weight=old_font.GetWeight(), underline=old_font.GetUnderlined(), faceName=old_font.GetFaceName(), encoding=old_font.GetDefaultEncoding())
        new_font.SetPointSize(new_font_size)
        control.SetFont(new_font)
    if isinstance(control, wx._controls.StaticText):
        control.Wrap(320)
    for child in control.GetChildren():
        fix_text_sizes(child)