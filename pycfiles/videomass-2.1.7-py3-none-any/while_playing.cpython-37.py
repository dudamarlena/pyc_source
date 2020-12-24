# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_frames/while_playing.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 4460 bytes
import wx
keys = _('q, ESC\nf\np, SPC\nm\n9, 0\n/, *\na\nv\nt\nc\nw\ns\n\nleft/right\ndown/up\npage down/page up\n\nright mouse click\nleft mouse double-click')
explan = _('Quiet.\nTogle full screen.\nPause.\nTogle mute.\nDecrease and increase volume respectively.\nDecrease and increase volume respectively.\nCycle audio channel in the current program.\nCycle video channel.\nCycle subtitle channel in the current program.\nCycle program.\nCycle video filters or show modes.\nStep to the next frame. Pause if the stream is not \nalready paused, step to the next video frame, and pause.\nSeek backward/forward 10 seconds.\nSeek backward/forward 1 minute.\nSeek to the previous/next chapter. Or if there are no \nchapters Seek backward/forward 10 minutes.\nSeek to percentage in file corresponding to fraction of width.\nToggle full screen.')

class While_Playing(wx.MiniFrame):
    __doc__ = '\n    Display a dialog box resizable with shortcuts keyboard\n    useful when you use playback function with FFplay\n\n    '

    def __init__(self, OS):
        wx.MiniFrame.__init__(self, None, style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        label1 = wx.StaticText(panel, wx.ID_ANY, keys)
        label2 = wx.StaticText(panel, wx.ID_ANY, explan)
        self.button_close = wx.Button(self, wx.ID_CLOSE, '')
        self.SetTitle(_('Videomass: Shortcuts while playing'))
        label1.SetForegroundColour(wx.Colour('#008000'))
        label2.SetForegroundColour(wx.Colour('#959595'))
        panel.SetBackgroundColour(wx.Colour('#121212'))
        s1 = wx.BoxSizer(wx.VERTICAL)
        gr_s1 = wx.FlexGridSizer(1, 2, 0, 0)
        gr_s1.Add(label1, 0, wx.ALL, 5)
        gr_s1.Add(label2, 0, wx.ALL, 5)
        btngrid = wx.FlexGridSizer(1, 1, 0, 0)
        btngrid.Add(self.button_close, 0, wx.ALL, 5)
        panel.SetSizer(gr_s1)
        s1.Add(panel, 0)
        s1.Add(btngrid, flag=(wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT), border=5)
        self.SetSizerAndFit(s1)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        """
        destroy dialog by button and the X
        """
        self.Destroy()