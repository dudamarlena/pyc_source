# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/edit_attachement_frame.py
# Compiled at: 2018-04-29 13:42:48
from dialogs.dialog_edit_attachement import DialogEditAttachement
import wx, rest, os
from configuration import Configuration
import webbrowser
from helper.exception import print_stack

class EditAttachementFrame(DialogEditAttachement):

    def __init__(self, parent):
        super(EditAttachementFrame, self).__init__(parent)
        self.local_file = ''
        self.attachement = None
        return

    def addAttachement(self, type):
        self.Title = 'Add attachement'
        self.button_validate.LabelText = 'Add'
        result = self.ShowModal()
        if result == wx.ID_OK:
            attachement = type(id=self.attachement.id, description=self.text_description.Value, source_name=self.attachement.source_name, storage_path=self.attachement.storage_path)
            return attachement
        else:
            return

    def editAttachement(self, attachement):
        self.Title = 'Edit attachement'
        self.button_validate.LabelText = 'Apply'
        self.attachement = attachement
        self.button_open_file.Label = attachement.source_name
        self.text_description.Value = attachement.description
        result = self.ShowModal()
        if result == wx.ID_OK:
            attachement.id = self.attachement.id
            attachement.description = self.text_description.Value
            return attachement
        else:
            return

    def onButtonOpenFileClick(self, event):
        configuration = Configuration()
        if self.button_open_file.Label != '<None>':
            url = os.path.join(configuration.kipartbase, 'file', self.attachement.storage_path)
            url = url.replace('\\', '/')
            webbrowser.open(url)

    def onButtonAddFileClick(self, event):
        dlg = wx.FileDialog(self, message='Choose a file', defaultDir=os.getcwd(), defaultFile='', wildcard='Symbol (*)|*', style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            self.button_open_file.Label = os.path.basename(dlg.GetPath())
            self.local_file = os.path.basename(dlg.GetPath())

    def onValidateClick(self, event):
        try:
            if self.local_file == '' and self.attachement is None:
                wx.MessageBox('No file selected', 'Error', wx.OK | wx.ICON_ERROR)
            elif self.local_file:
                attachement = rest.api.add_upload_file(upfile=self.local_file)
                if self.attachement is None:
                    self.attachement = rest.model.PartAttachement(id=attachement.id)
                self.attachement.id = attachement.id
                self.attachement.source_name = attachement.source_name
                self.attachement.storage_path = attachement.storage_path
                self.EndModal(wx.ID_OK)
            else:
                self.EndModal(wx.ID_OK)
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return

        return

    def onCancelClick(self, event):
        self.EndModal(wx.ID_CANCEL)