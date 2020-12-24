# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableMessage.py
# Compiled at: 2016-07-01 03:18:09
"""
Class OWTextableMessage
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
__version__ = '0.01.2'
import json
from LTTL.Segmentation import Segmentation
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableMessage(OWWidget):
    """Orange widget for parsing JSON data in segmentation"""
    settingsList = [
     'autoSend',
     'uuid']

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Message widget"""
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Segmentation', Segmentation, self.inputData, Single)]
        self.outputs = [('Message', JSONMessage, Single)]
        self.autoSend = True
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentation = None
        self.infoBox = InfoBox(widget=self.controlArea)
        OWGUI.separator(self.controlArea, height=3)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox')
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.setMinimumWidth(150)
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def inputData(self, newInput):
        """Process incoming data"""
        self.segmentation = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()

    def sendData(self):
        """Parse JSON data and send message"""
        if not self.segmentation:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Message', None, self)
            return
        else:
            if len(self.segmentation) > 1:
                self.infoBox.setText('Please make sure that input contains only one segment.', 'error')
                self.send('Message', None, self)
                return
            self.infoBox.inputChanged()
            try:
                content = self.segmentation[0].get_content()
                jsonList = json.loads(content)
                jsonMessage = JSONMessage(content)
                message = '%i item@p sent to output.' % len(jsonList)
                message = pluralize(message, len(jsonList))
                self.infoBox.setText(message)
                self.send('Message', jsonMessage, self)
            except ValueError:
                self.infoBox.setText('Please make sure that input contains valid JSON data.', 'error')
                self.send('Segmented data', None, self)
                self.send('Message', None, self)
                return

            self.sendButton.resetSettingsChangedFlag()
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
    ow = OWTextableMessage()
    ow.show()
    appl.exec_()