# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datapkggui/gui/packagegui.py
# Compiled at: 2011-10-24 14:58:37
__author__ = 'dgraziotin'
import wx, wx.xrc, datapkg, datapkggui.lib as lib, datapkggui.operations as operations, base

class PackageGUI(base.GUI):

    def __init__(self, xml, package=None):
        base.GUI.__init__(self, xml, frame_name='InfoFrame', panel_name='panel')
        self.m_frame.SetSize(wx.Size(500, 500))
        self.m_download_button = self.GetWidget('download_button')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDownloadClick, 'download_button')
        if not package:
            package = datapkg.package.Package()
        self.m_package = package
        for key, value in lib.info(package, request_for='metadata').iteritems():
            setattr(self, key + '_text', wx.xrc.XRCCTRL(self.m_frame, key + '_text'))

        self.UpdateWidgets(package)
        self.m_status_bar.Hide()

    def UpdateWidgets(self, package):
        for key, value in lib.info(package, request_for='metadata').iteritems():
            try:
                text_ctrl = getattr(self, key + '_text')
                if key == 'tags':
                    tags = value
                    if tags:
                        for tag in tags:
                            self.tags_text.AppendText(tag + ' ')

                elif value:
                    text_ctrl.SetValue(unicode(value))
                else:
                    text_ctrl.SetValue('N/A')
            except AttributeError:
                continue

    def OnButtonDownloadClick(self, event):
        """
        Retrieve the currently selected package in the results list and launch a DownloadOperation
        for downloading it.
        """
        download_dir = self.DownloadDirDialog()
        if self.m_package and download_dir:
            operations.DownloadOperation(self.m_frame, self.m_package, download_dir)
            self.Show(False)