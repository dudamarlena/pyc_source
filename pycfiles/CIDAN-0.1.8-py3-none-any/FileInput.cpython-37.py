# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Inputs/FileInput.py
# Compiled at: 2020-04-29 16:26:46
# Size of source mod 2**32: 2406 bytes
from PySide2 import QtCore
from PySide2.QtWidgets import *
import CIDAN.GUI.Inputs.Input as Input

class FileInput(Input):

    def __init__(self, display_name, program_name, on_change_function, default_val, tool_tip, isFolder, forOpen):
        super().__init__(display_name, program_name, on_change_function, default_val, tool_tip)
        self.isFolder = isFolder
        self.forOpen = forOpen
        self.path = ''
        self.current_location = QLabel()
        self.current_location.setText('')
        self.layout_h.addWidget(self.current_location)
        self.button = QPushButton()
        self.button.setText('Browse')
        self.button.clicked.connect(self.on_browse_button)
        self.button.setToolTip(tool_tip)
        self.layout_h.addWidget(self.button)

    def on_browse_button(self):
        self.path = createFileDialog(directory='~/Desktop', forOpen=(self.forOpen), isFolder=(self.isFolder))
        self.current_location.setText(self.path)
        if self.on_change_function != None:
            self.on_change_function(self.path)

    def current_state(self):
        return self.path


def createFileDialog(directory='', forOpen=True, fmt='', isFolder=0):
    directory = '/Users/sschickler/Documents/LSSC-python/input_images'
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)
    dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
    if isFolder == 1:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
    if isFolder == 2:
        dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)
    if fmt != '':
        if isFolder is False:
            dialog.setDefaultSuffix(fmt)
            dialog.setNameFilters([f"{fmt} (*.{fmt})"])
    if directory != '':
        dialog.setDirectory(str(directory))
    if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]
        return path
    return ''