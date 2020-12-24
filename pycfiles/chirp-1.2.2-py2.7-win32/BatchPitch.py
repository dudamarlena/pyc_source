# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\gui\BatchPitch.py
# Compiled at: 2013-12-11 23:17:46
"""
Dialog for running batch pitch comparisons.

Copyright (C) 2012 Daniel Meliza <dmeliza@dylan.uchicago.edu>
Created 2012-02-13
"""
import os, wx
from chirp.gui.events import EVT_COUNT, BatchEvent, BatchConsumer, threading
from chirp.pitch import batch

class FileListBox(wx.Panel):
    """
    A panel with a ListBox and two buttons to add and remove files
    from the list
    """

    def __init__(self, parent=None, id=-1, wildcard='WAV files (*.wav)|*.wav'):
        wx.Panel.__init__(self, parent, id)
        self.wildcard = wildcard
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_list = wx.ListBox(self, -1, style=wx.LB_EXTENDED)
        hbox1.Add(self.file_list, 1, wx.EXPAND)
        vbox.Add(hbox1, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        add = wx.Button(self, -1, 'Add Files', size=(100, -1))
        remove = wx.Button(self, -1, 'Remove Files', size=(100, -1))
        self.Bind(wx.EVT_BUTTON, self.on_add, id=add.GetId())
        self.Bind(wx.EVT_BUTTON, self.on_del, id=remove.GetId())
        hbox2.Add(add, 0, wx.ALL, 2)
        hbox2.Add(remove, 0, wx.ALL, 2)
        vbox.Add(hbox2, 0)
        self.SetSizer(vbox)

    @property
    def files(self):
        return self.file_list.GetStrings()

    def on_add(self, event):
        fdlg = wx.FileDialog(self, 'Select one or more files', wildcard=self.wildcard, style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST)
        val = fdlg.ShowModal()
        if val == wx.ID_OK:
            current = self.file_list.GetStrings()
            fdir = fdlg.GetDirectory()
            for x in fdlg.GetFilenames():
                if x not in current:
                    self.file_list.Append(os.path.join(fdir, x))

    def on_del(self, event):
        for x in reversed(sorted(self.file_list.GetSelections())):
            self.file_list.Delete(x)


class BatchPitch(wx.Frame):
    _inactive_controls = ('file_list', 'config', 'usemask', 'skipcompl', 'nworkers',
                          'btn_start')

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, title='Batch Pitch Estimation', size=(400,
                                                                              500), style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.create_main_panel()
        self.batch_thread = None
        return

    def create_main_panel(self):
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        mainPanel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(mainPanel, -1, 'Select files to analyze:')
        txt.SetFont(font)
        vbox.Add(txt, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.file_list = FileListBox(mainPanel, -1)
        vbox.Add(self.file_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        txt = wx.StaticText(mainPanel, -1, 'Select configuration file:')
        txt.SetFont(font)
        vbox.Add(txt, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.config = wx.FilePickerCtrl(mainPanel, -1, message='Select configuration file', wildcard='CFG files (*.cfg)|*.cfg', style=wx.FLP_OPEN | wx.FLP_FILE_MUST_EXIST | wx.FLP_USE_TEXTCTRL)
        vbox.Add(self.config, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(mainPanel, -1, 'Number of processes to run:')
        txt.SetFont(font)
        hbox.Add(txt, 0, wx.ALIGN_CENTER)
        self.nworkers = wx.SpinCtrl(mainPanel, -1, size=(60, -1))
        self.nworkers.SetRange(1, batch.multiprocessing.cpu_count())
        self.nworkers.SetValue(1)
        hbox.Add(self.nworkers, 0, wx.LEFT, 5)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(mainPanel, -1, 'Use mask files if they exist:')
        txt.SetFont(font)
        hbox.Add(txt, 0, wx.ALIGN_CENTER)
        self.usemask = wx.CheckBox(mainPanel, -1)
        self.usemask.SetValue(1)
        hbox.Add(self.usemask, 0, wx.LEFT, 5)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(mainPanel, -1, 'Skip completed:')
        txt.SetFont(font)
        hbox.Add(txt, 0, wx.ALIGN_CENTER)
        self.skipcompl = wx.CheckBox(mainPanel, -1)
        self.skipcompl.SetValue(1)
        hbox.Add(self.skipcompl, 0, wx.LEFT, 5)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        vbox.Add((-1, 10))
        txt = wx.StaticText(mainPanel, -1, 'Progress:')
        txt.SetFont(font)
        vbox.Add(txt, 0, wx.LEFT, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.gauge = wx.Gauge(mainPanel, -1)
        hbox.Add(self.gauge, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_start = wx.Button(mainPanel, wx.ID_OK, 'Start', size=(100, -1))
        self.btn_cancel = wx.Button(mainPanel, wx.ID_CANCEL, 'Close', size=(100, -1))
        self.Bind(wx.EVT_BUTTON, self.on_start, id=self.btn_start.GetId())
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=self.btn_cancel.GetId())
        hbox.Add(self.btn_start, 0, wx.RIGHT, 5)
        hbox.Add(self.btn_cancel)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.Bind(EVT_COUNT, self.on_batch_update)
        self.status = wx.StatusBar(mainPanel, -1)
        vbox.Add(self.status, 0, wx.EXPAND)
        mainPanel.SetSizer(vbox)

    def on_start(self, event):
        files = self.file_list.files
        nfiles = len(files)
        if len(files) == 0:
            self.status.SetStatusText('No files selected')
            return
        else:
            cfg = self.config.GetPath()
            if len(cfg) == 0:
                cfg = None
            mask = self.usemask.GetValue()
            skip = self.skipcompl.GetValue()
            nw = self.nworkers.GetValue()
            self._disable_interface()
            self.gauge.SetRange(nfiles)
            self.gauge.SetValue(0)
            self.status.SetStatusText('Batch running...')
            try:
                self.batch_consumer = BatchConsumer(self)
                batch.run(files, self.batch_consumer, config=cfg, workers=nw, mask=mask, skip=skip)
                self.batch_thread = threading.Thread(target=self.batch_consumer)
                self.batch_thread.daemon = True
                self.batch_thread.start()
            except Exception as e:
                self._enable_interface()
                self.status.SetStatusText('Error: %s' % e)

            return

    def on_batch_update(self, event):
        value = event.GetValue()
        if value is not None:
            self.gauge.SetValue(value + 1)
        else:
            self.status.SetStatusText('Batch finished (%d/%d completed)' % (self.gauge.GetValue(),
             self.gauge.GetRange()))
            self.gauge.SetValue(self.gauge.GetRange())
            self._enable_interface()
        return

    def on_cancel(self, event):
        if self.batch_thread is None or not self.batch_thread.is_alive():
            self.Destroy()
        else:
            self.status.SetStatusText('Canceling batch after current jobs finish...')
            self.batch_consumer.stop()
            wx.BeginBusyCursor()
        return

    def _disable_interface(self):
        for ctrl in self._inactive_controls:
            getattr(self, ctrl).Disable()

        self.btn_cancel.SetLabel('Cancel')

    def _enable_interface(self):
        self.btn_cancel.SetLabel('Close')
        self.btn_cancel.Enable()
        try:
            wx.EndBusyCursor()
        except:
            pass

        for ctrl in self._inactive_controls:
            getattr(self, ctrl).Enable()


def test():
    app = wx.PySimpleApp()
    app.frame = BatchPitch()
    app.frame.Show()
    app.MainLoop()