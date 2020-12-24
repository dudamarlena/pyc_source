# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_dialogs/popup.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 3499 bytes
import wx
from pubsub import pub

class PopupDialog(wx.Dialog):
    __doc__ = '\n    A pop-up dialog box for temporary user messages that tell the user\n    the load in progress (required for large files).\n\n    Usage:\n            loadDlg = PopupDialog(None, ("Videomass - Loading"),\n                                  ("\nWait....\nwork in progress.\n")\n                                  )\n            loadDlg.ShowModal()\n            loadDlg.Destroy()\n    '

    def __init__(self, parent, title, msg):
        wx.Dialog.__init__(self, parent, (-1), title, size=(350, 150), style=(wx.CAPTION))
        box = wx.BoxSizer(wx.VERTICAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        bitmap = wx.Bitmap(32, 32)
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MESSAGE_BOX, (32,
                                                                                   32))
        graphic = wx.StaticBitmap(self, -1, bitmap)
        box2.Add(graphic, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        message = wx.StaticText(self, -1, msg)
        box2.Add(message, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        box.Add(box2, 0, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Fit()
        self.Layout()
        pub.subscribe(self.getMessage, 'RESULT_EVT')

    def getMessage(self, status):
        """
        Riceive msg and status from thread.
        All'inizio usavo self.Destroy() per chiudere il dialogo modale
        (con modeless ritornava dati None), ma dava warning e critical
        e su OsX non chiudeva affatto. Con EndModal ho risolto tutti
        i problemi e funziona bene. Ma devi ricordarti di eseguire
        Destroy() dopo ShowModal() nel chiamante.
        vedi: https://github.com/wxWidgets/Phoenix/issues/672
        Penso sia fattibile anche implementare un'interfaccia GetValue
        su questo dialogo, ma si perderebbe un po' di portabilità.
        """
        self.EndModal(1)