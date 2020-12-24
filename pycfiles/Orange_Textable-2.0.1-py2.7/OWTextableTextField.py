# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableTextField.py
# Compiled at: 2016-07-02 05:20:44
"""
Class OWTextableTextField
Copyright 2012-2016 LangTech Sarl (info@langtech.ch)
-----------------------------------------------------------------------------
This file is part of the Orange-Textable package v2.0.

Orange-Textable v2.0 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orange-Textable v2.0 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orange-Textable v2.0. If not, see <http://www.gnu.org/licenses/>.
"""
__version__ = '0.13.3'
from unicodedata import normalize
from PyQt4 import QtCore
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableTextField(OWWidget):
    """Orange widget for typing text data"""
    settingsList = [
     'textFieldContent',
     'encoding',
     'autoSend',
     'uuid']
    encodings = getPredefinedEncodings()

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Text File widget"""
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Text data', Segmentation, self.inputTextData, Single)]
        self.outputs = [('Text data', Segmentation)]
        self.textFieldContent = ('').encode('utf-8')
        self.encoding = 'utf-8'
        self.autoSend = True
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.adjustSize())
        self.segmentation = Input(text='')
        OWGUI.separator(widget=self.controlArea, height=3)
        self.editor = QPlainTextEdit()
        self.editor.setPlainText(self.textFieldContent.decode('utf-8'))
        self.controlArea.layout().addWidget(self.editor)
        self.connect(self.editor, SIGNAL('textChanged()'), self.sendButton.settingsChanged)
        OWGUI.separator(widget=self.controlArea, height=3)
        self.setMinimumWidth(250)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        return

    def inputTextData(self, segmentation):
        """Handle text data on input connection"""
        self.segmentation.clear()
        if not segmentation:
            return
        self.editor.setPlainText(('').join([ s.get_content() for s in segmentation ]))
        self.sendButton.settingsChanged()

    def sendData(self):
        """Normalize content, then create and send segmentation"""
        textFieldContent = unicode(QtCore.QTextCodec.codecForName('UTF-16').fromUnicode(self.editor.toPlainText()), 'UTF-16')
        self.textFieldContent = textFieldContent.encode('utf-8')
        textFieldContent = textFieldContent.replace('\r\n', '\n').replace('\r', '\n')
        textFieldContent = normalize('NFC', textFieldContent)
        if not self.textFieldContent:
            self.infoBox.setText(message='Please type or paste some text above.', state='warning')
            self.send('Text data', None, self)
            return
        else:
            message = '1 segment (%i character@p) sent to output.' % len(textFieldContent)
            message = pluralize(message, len(textFieldContent))
            self.infoBox.setText(message)
            self.segmentation.update(textFieldContent, label=self.captionTitle)
            self.send('Text data', self.segmentation, self)
            self.sendButton.resetSettingsChangedFlag()
            return

    def setCaption(self, title):
        if 'captionTitle' in dir(self) and title != 'Orange Widget':
            OWWidget.setCaption(self, title)
            self.sendButton.settingsChanged()
        else:
            OWWidget.setCaption(self, title)

    def onDeleteWidget(self):
        if self.segmentation is not None:
            self.segmentation.clear()
        return

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def getSettings(self, *args, **kwargs):
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings['settingsDataVersion'] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        if settings.get('settingsDataVersion', None) == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings['settingsDataVersion']
            OWWidget.setSettings(self, settings)
        return


if __name__ == '__main__':
    appl = QApplication(sys.argv)
    ow = OWTextableTextField()
    ow.show()
    appl.exec_()
    ow.saveSettings()