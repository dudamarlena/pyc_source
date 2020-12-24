# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/samples/wxwrapdemo.py
# Compiled at: 2018-07-23 18:20:27
"""Text wrapping demo on uniseg + wxPython """
from __future__ import absolute_import, division, print_function, unicode_literals
from locale import getpreferredencoding
import wx
from uniseg.wrap import wrap, Formatter
default_text = b"The quick (“brown”) fox can’t jump 32.3 feet, right?\n\nAlice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'\n\n虎梵名ヴィヤグラ、今のインド語でバグ、南インドのタミル語でピリ、ジャワ名マチャム、マレー名リマウ、アラブ名ニムル、英語でタイガー、その他欧州諸国大抵これに似おり、いずれもギリシアやラテンのチグリスに基づく。そのチグリスなる名は古ペルシア語のチグリ（箭）より出で、虎の駛く走るを箭の飛ぶに比べたるに因るならんという。わが国でも古来虎を実際見ずに千里を走ると信じ、戯曲に清正の捷疾を賞して千里一跳虎之助などと洒落て居る。プリニの『博物志』に拠れば生きた虎をローマ人が初めて見たのはアウグスッス帝の代だった。\n"
_preferredencoding = getpreferredencoding()

class SampleWxFormatter(Formatter):

    def __init__(self, dc, log_width):
        self._dc = dc
        self._log_width = log_width
        self._log_cur_x = 0
        self._log_cur_y = 0

    @property
    def wrap_width(self):
        return self._log_width

    def reset(self):
        self._log_cur_x = 0
        self._log_cur_y = 0

    def text_extents(self, s):
        dc = self._dc
        return dc.GetPartialTextExtents(s)

    def handle_text(self, text, extents):
        if not text or not extents:
            return
        dc = self._dc
        dc.DrawText(text, self._log_cur_x, self._log_cur_y)
        self._log_cur_x += extents[(-1)]

    def handle_new_line(self):
        dc = self._dc
        log_line_height = dc.GetCharHeight()
        self._log_cur_y += log_line_height
        self._log_cur_x = 0


class App(wx.App):

    def OnInit(self):
        frame = Frame(None, wx.ID_ANY, __file__)
        self.SetTopWindow(frame)
        frame.Show()
        return True


class Frame(wx.Frame):
    ID_FONT = wx.NewId()

    def __init__(self, parent, id_, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=b'frame'):
        wx.Frame.__init__(self, parent, id_, title, pos, size, style, name)
        self.Bind(wx.EVT_MENU, self.OnCmdOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnCmdExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnCmdFont, id=self.ID_FONT)
        menubar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_OPEN, b'&Open')
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, b'&Exit')
        menubar.Append(menu, b'&File')
        menu = wx.Menu()
        menu.Append(self.ID_FONT, b'&Font...')
        menubar.Append(menu, b'F&ormat')
        self.SetMenuBar(menubar)
        self.wrap_window = WrapWindow(self, wx.ID_ANY)

    def OnCmdOpen(self, evt):
        filename = wx.FileSelector(b'Open')
        if not filename:
            return
        raw_text = open(filename, b'rU').read()
        for enc in {b'utf-8', _preferredencoding}:
            try:
                text = raw_text.decode(enc)
            except UnicodeDecodeError:
                continue
            else:
                break

        else:
            wx.MessageBox(b"Couldn't open this file.", b'Open', wx.ICON_ERROR)
            return

        self.wrap_window.SetText(text)
        self.wrap_window.Refresh()

    def OnCmdExit(self, evt):
        self.Close()

    def OnCmdFont(self, evt):
        data = wx.FontData()
        font = self.wrap_window.GetFont()
        data.SetInitialFont(font)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            ret_data = dlg.GetFontData()
            ret_font = ret_data.GetChosenFont()
            self.wrap_window.SetFont(ret_font)
            self.wrap_window.Refresh()


class WrapWindow(wx.Window):
    _text = default_text
    _default_fontface = b'Times New Roman'
    _default_fontsize = 18

    def __init__(self, parent, id_, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name=wx.PanelNameStr):
        wx.Window.__init__(self, parent, id_, pos, size, style, name)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetBackgroundColour(wx.WHITE)
        self.SetForegroundColour(wx.BLACK)
        font = wx.Font(self._default_fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, self._default_fontface)
        self.SetFont(font)

    def GetText(self, value):
        return _text

    def SetText(self, value):
        self._text = value

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        font = self.GetFont()
        dc.SetFont(font)
        dev_width, dev_height = self.GetClientSize()
        log_width = dc.DeviceToLogicalX(dev_width)
        log_height = dc.DeviceToLogicalY(dev_height)
        formatter = SampleWxFormatter(dc, log_width)
        wrap(formatter, self._text)

    def OnSize(self, evt):
        self.Refresh()


def main():
    app = App(0)
    app.MainLoop()


if __name__ == b'__main__':
    main()