# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableURLs.py
# Compiled at: 2016-08-11 09:23:10
"""
Class OWTextableURLs
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
__version__ = '0.14.2'
import codecs, urllib, re, json
from unicodedata import normalize
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
import LTTL.Segmenter as Segmenter
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableURLs(OWWidget):
    """Orange widget for fetching text from URLs"""
    settingsList = [
     'URLs',
     'encoding',
     'autoSend',
     'autoNumber',
     'autoNumberKey',
     'importURLs',
     'importURLsKey',
     'displayAdvancedSettings',
     'lastLocation',
     'URL',
     'uuid']

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Message', JSONMessage, self.inputMessage, Single)]
        self.outputs = [
         (
          'Text data', Segmentation)]
        self.URLs = list()
        self.encoding = 'utf-8'
        self.autoSend = True
        self.autoNumber = False
        self.autoNumberKey = 'num'
        self.importURLs = True
        self.importURLsKey = 'url'
        self.lastLocation = '.'
        self.displayAdvancedSettings = False
        self.URL = ''
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentation = None
        self.createdInputs = list()
        self.URLLabel = list()
        self.selectedURLLabel = list()
        self.newURL = ''
        self.newAnnotationKey = ''
        self.newAnnotationValue = ''
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.updateGUI)
        self.advancedSettings = AdvancedSettings(widget=self.controlArea, master=self, callback=self.sendButton.settingsChanged)
        self.advancedSettings.draw()
        basicURLBox = OWGUI.widgetBox(widget=self.controlArea, box='Source', orientation='vertical')
        basicURLBoxLine1 = OWGUI.widgetBox(widget=basicURLBox, box=False, orientation='horizontal')
        OWGUI.lineEdit(widget=basicURLBoxLine1, master=self, value='URL', orientation='horizontal', label='URL:', labelWidth=101, callback=self.sendButton.settingsChanged, tooltip='The URL whose content will be imported.')
        OWGUI.separator(widget=basicURLBox, height=3)
        OWGUI.comboBox(widget=basicURLBox, master=self, value='encoding', items=getPredefinedEncodings(), sendSelectedValue=True, orientation='horizontal', label='Encoding:', labelWidth=101, callback=self.sendButton.settingsChanged, tooltip="Select URL's encoding.")
        OWGUI.separator(widget=basicURLBox, height=3)
        self.advancedSettings.basicWidgets.append(basicURLBox)
        self.advancedSettings.basicWidgetsAppendSeparator()
        URLBox = OWGUI.widgetBox(widget=self.controlArea, box='Sources', orientation='vertical')
        URLBoxLine1 = OWGUI.widgetBox(widget=URLBox, box=False, orientation='horizontal', addSpace=True)
        self.fileListbox = OWGUI.listBox(widget=URLBoxLine1, master=self, value='selectedURLLabel', labels='URLLabel', callback=self.updateURLBoxButtons, tooltip='The list of URLs whose content will be imported.\n\nIn the output segmentation, the content of each\nURL appears in the same position as in the list.\n\nColumn 1 shows the URL.\nColumn 2 shows the associated annotation (if any).\nColumn 3 shows the associated encoding.')
        font = QFont()
        font.setFamily('Courier')
        font.setStyleHint(QFont.Courier)
        font.setPixelSize(12)
        self.fileListbox.setFont(font)
        URLBoxCol2 = OWGUI.widgetBox(widget=URLBoxLine1, orientation='vertical')
        self.moveUpButton = OWGUI.button(widget=URLBoxCol2, master=self, label='Move Up', callback=self.moveUp, tooltip='Move the selected URL upward in the list.')
        self.moveDownButton = OWGUI.button(widget=URLBoxCol2, master=self, label='Move Down', callback=self.moveDown, tooltip='Move the selected URL downward in the list.')
        self.removeButton = OWGUI.button(widget=URLBoxCol2, master=self, label='Remove', callback=self.remove, tooltip='Remove the selected URL from the list.')
        self.clearAllButton = OWGUI.button(widget=URLBoxCol2, master=self, label='Clear All', callback=self.clearAll, tooltip='Remove all URLs from the list.')
        self.exportButton = OWGUI.button(widget=URLBoxCol2, master=self, label='Export List', callback=self.exportList, tooltip='Open a dialog for selecting a file where the URL\nlist can be exported in JSON format.')
        self.importButton = OWGUI.button(widget=URLBoxCol2, master=self, label='Import List', callback=self.importList, tooltip='Open a dialog for selecting an URL list to\nimport (in JSON format). URLs from this list will\nbe added to those already imported.')
        URLBoxLine2 = OWGUI.widgetBox(widget=URLBox, box=False, orientation='vertical')
        addURLBox = OWGUI.widgetBox(widget=URLBoxLine2, box=True, orientation='vertical')
        OWGUI.lineEdit(widget=addURLBox, master=self, value='newURL', orientation='horizontal', label='URL(s):', labelWidth=101, callback=self.updateGUI, tooltip="The URL(s) that will be added to the list when\nbutton 'Add' is clicked.\n\nSuccessive URLs must be separated with ' / ' \n(space + slash + space). Their order in the list\n will be the same as in this field.")
        OWGUI.separator(widget=addURLBox, height=3)
        OWGUI.comboBox(widget=addURLBox, master=self, value='encoding', items=getPredefinedEncodings(), sendSelectedValue=True, orientation='horizontal', label='Encoding:', labelWidth=101, callback=self.updateGUI, tooltip="Select URL's encoding.")
        OWGUI.separator(widget=addURLBox, height=3)
        OWGUI.lineEdit(widget=addURLBox, master=self, value='newAnnotationKey', orientation='horizontal', label='Annotation key:', labelWidth=101, callback=self.updateGUI, tooltip='This field lets you specify a custom annotation\nkey associated with each URL that is about to be\nadded to the list.')
        OWGUI.separator(widget=addURLBox, height=3)
        OWGUI.lineEdit(widget=addURLBox, master=self, value='newAnnotationValue', orientation='horizontal', label='Annotation value:', labelWidth=101, callback=self.updateGUI, tooltip='This field lets you specify the annotation value\nassociated with the above annotation key.')
        OWGUI.separator(widget=addURLBox, height=3)
        self.addButton = OWGUI.button(widget=addURLBox, master=self, label='Add', callback=self.add, tooltip="Add the URL currently displayed in the 'URL'\ntext field to the list.")
        self.advancedSettings.advancedWidgets.append(URLBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        optionsBox = OWGUI.widgetBox(widget=self.controlArea, box='Options', orientation='vertical')
        optionsBoxLine1 = OWGUI.widgetBox(widget=optionsBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=optionsBoxLine1, master=self, value='importURLs', label='Import URLs with key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Import URLs as annotations.')
        self.importURLsKeyLineEdit = OWGUI.lineEdit(widget=optionsBoxLine1, master=self, value='importURLsKey', orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='Annotation key for importing URLs.')
        OWGUI.separator(widget=optionsBox, height=3)
        optionsBoxLine2 = OWGUI.widgetBox(widget=optionsBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=optionsBoxLine2, master=self, value='autoNumber', label='Auto-number with key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Annotate URLs with increasing numeric indices.')
        self.autoNumberKeyLineEdit = OWGUI.lineEdit(widget=optionsBoxLine2, master=self, value='autoNumberKey', orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='Annotation key for URL auto-numbering.')
        OWGUI.separator(widget=optionsBox, height=3)
        self.advancedSettings.advancedWidgets.append(optionsBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def inputMessage(self, message):
        """Handle JSON message on input connection"""
        if not message:
            return
        else:
            self.displayAdvancedSettings = True
            self.advancedSettings.setVisible(True)
            self.clearAll()
            self.infoBox.inputChanged()
            try:
                json_data = json.loads(message.content)
                temp_URLs = list()
                for entry in json_data:
                    URL = entry.get('url', '')
                    encoding = entry.get('encoding', '')
                    annotationKey = entry.get('annotation_key', '')
                    annotationValue = entry.get('annotation_value', '')
                    if URL == '' or encoding == '':
                        self.infoBox.setText('Please verify keys and values of incoming JSON message.', 'error')
                        self.send('Text data', None, self)
                        return
                    temp_URLs.append((
                     URL,
                     encoding,
                     annotationKey,
                     annotationValue))

                self.URLs.extend(temp_URLs)
                self.sendButton.settingsChanged()
            except ValueError:
                self.infoBox.setText('Please make sure that incoming message is valid JSON.', 'error')
                self.send('Text data', None, self)
                return

            return

    def sendData(self):
        """Fetch URL content, create and send segmentation"""
        if self.displayAdvancedSettings and not self.URLs or not (self.URL or self.displayAdvancedSettings):
            self.infoBox.setText('Please select source URL.', 'warning')
            self.send('Text data', None, self)
            return
        else:
            if self.displayAdvancedSettings and self.autoNumber:
                if self.autoNumberKey:
                    autoNumberKey = self.autoNumberKey
                else:
                    self.infoBox.setText('Please enter an annotation key for auto-numbering.', 'warning')
                    self.send('Text data', None, self)
                    return
            else:
                autoNumberKey = None
            self.clearCreatedInputs()
            URLContents = list()
            annotations = list()
            counter = 1
            if self.displayAdvancedSettings:
                myURLs = self.URLs
            else:
                myURLs = [
                 [
                  self.URL, self.encoding, '', '']]
            progressBar = OWGUI.ProgressBar(self, iterations=len(myURLs))
            for myURL in myURLs:
                URL = myURL[0]
                encoding = myURL[1]
                annotation_key = myURL[2]
                annotation_value = myURL[3]
                self.error()
                try:
                    URLHandle = urllib.urlopen(URL)
                    try:
                        try:
                            URLContent = URLHandle.read().decode(encoding)
                        except UnicodeError:
                            progressBar.finish()
                            if len(myURLs) > 1:
                                message = 'Please select another encoding ' + 'for URL %s.' % URL
                            else:
                                message = 'Please select another encoding.'
                            self.infoBox.setText(message, 'error')
                            self.send('Text data', None, self)
                            return

                    finally:
                        URLHandle.close()

                except IOError:
                    progressBar.finish()
                    if len(myURLs) > 1:
                        message = "Couldn't retrieve %s." % URL
                    else:
                        message = "Couldn't retrieve URL."
                    self.infoBox.setText(message, 'error')
                    self.send('Text data', None, self)
                    return

                URLContent = ('\n').join(URLContent.splitlines())
                if encoding == 'utf-8':
                    URLContent = URLContent.lstrip(unicode(codecs.BOM_UTF8, 'utf-8'))
                URLContent = normalize('NFC', URLContent)
                URLContents.append(URLContent)
                annotation = dict()
                if self.displayAdvancedSettings:
                    if annotation_key and annotation_value:
                        annotation[annotation_key] = annotation_value
                    if self.importURLs and self.importURLsKey:
                        annotation[self.importURLsKey] = URL
                    if self.autoNumber and self.autoNumberKey:
                        annotation[self.autoNumberKey] = counter
                        counter += 1
                annotations.append(annotation)
                progressBar.advance()

            if len(URLContents) == 1:
                label = self.captionTitle
            else:
                label = None
            for index in xrange(len(URLContents)):
                myInput = Input(URLContents[index], label)
                segment = myInput[0]
                segment.annotations.update(annotations[index])
                myInput[0] = segment
                self.createdInputs.append(myInput)

            if len(URLContents) == 1:
                self.segmentation = self.createdInputs[0]
            else:
                self.segmentation = Segmenter.concatenate(segmentations=self.createdInputs, label=self.captionTitle, copy_annotations=True, import_labels_as=None, sort=False, auto_number_as=None, merge_duplicates=False, progress_callback=None)
            message = '%i segment@p sent to output ' % len(self.segmentation)
            message = pluralize(message, len(self.segmentation))
            numChars = 0
            for segment in self.segmentation:
                segmentLength = len(Segmentation.get_data(segment.str_index))
                numChars += segmentLength

            message += '(%i character@p).' % numChars
            message = pluralize(message, numChars)
            self.infoBox.setText(message)
            progressBar.finish()
            self.send('Text data', self.segmentation, self)
            self.sendButton.resetSettingsChangedFlag()
            return

    def clearCreatedInputs(self):
        for i in self.createdInputs:
            Segmentation.set_data(i[0].str_index, None)

        del self.createdInputs[:]
        return

    def importList(self):
        """Display a FileDialog and import URL list"""
        filePath = unicode(QFileDialog.getOpenFileName(self, 'Import URL List', self.lastLocation, 'Text files (*)'))
        if not filePath:
            return
        else:
            self.file = os.path.normpath(filePath)
            self.lastLocation = os.path.dirname(filePath)
            self.error()
            try:
                fileHandle = codecs.open(filePath, encoding='utf8')
                fileContent = fileHandle.read()
                fileHandle.close()
            except IOError:
                QMessageBox.warning(None, 'Textable', "Couldn't open file.", QMessageBox.Ok)
                return

            try:
                json_data = json.loads(fileContent)
                temp_URLs = list()
                for entry in json_data:
                    URL = entry.get('url', '')
                    encoding = entry.get('encoding', '')
                    annotationKey = entry.get('annotation_key', '')
                    annotationValue = entry.get('annotation_value', '')
                    if URL == '' or encoding == '':
                        QMessageBox.warning(None, 'Textable', "Selected JSON file doesn't have the right keys and/or values.", QMessageBox.Ok)
                        return
                    temp_URLs.append((
                     URL,
                     encoding,
                     annotationKey,
                     annotationValue))

                self.URLs.extend(temp_URLs)
                if temp_URLs:
                    self.sendButton.settingsChanged()
            except ValueError:
                QMessageBox.warning(None, 'Textable', 'Selected file is not in JSON format.', QMessageBox.Ok)
                return

            return

    def exportList(self):
        """Display a FileDialog and export URL list"""
        toDump = list()
        for URL in self.URLs:
            toDump.append({'url': URL[0], 
               'encoding': URL[1]})
            if URL[2] and URL[3]:
                toDump[(-1)]['annotation_key'] = URL[2]
                toDump[(-1)]['annotation_value'] = URL[3]

        filePath = unicode(QFileDialog.getSaveFileName(self, 'Export URL List', self.lastLocation))
        if filePath:
            self.lastLocation = os.path.dirname(filePath)
            outputFile = codecs.open(filePath, encoding='utf8', mode='w', errors='xmlcharrefreplace')
            outputFile.write(normalizeCarriageReturns(json.dumps(toDump, sort_keys=True, indent=4)))
            outputFile.close()
            QMessageBox.information(None, 'Textable', 'URL list correctly exported', QMessageBox.Ok)
        return

    def moveUp(self):
        """Move URL upward in URLs listbox"""
        if self.selectedURLLabel:
            index = self.selectedURLLabel[0]
            if index > 0:
                temp = self.URLs[(index - 1)]
                self.URLs[index - 1] = self.URLs[index]
                self.URLs[index] = temp
                self.selectedURLLabel.listBox.item(index - 1).setSelected(1)
                self.sendButton.settingsChanged()

    def moveDown(self):
        """Move URL downward in URLs listbox"""
        if self.selectedURLLabel:
            index = self.selectedURLLabel[0]
            if index < len(self.URLs) - 1:
                temp = self.URLs[(index + 1)]
                self.URLs[index + 1] = self.URLs[index]
                self.URLs[index] = temp
                self.selectedURLLabel.listBox.item(index + 1).setSelected(1)
                self.sendButton.settingsChanged()

    def clearAll(self):
        """Remove all URLs from URLs attr"""
        del self.URLs[:]
        del self.selectedURLLabel[:]
        self.sendButton.settingsChanged()

    def remove(self):
        """Remove URL from URLs attr"""
        if self.selectedURLLabel:
            index = self.selectedURLLabel[0]
            self.URLs.pop(index)
            del self.selectedURLLabel[:]
            self.sendButton.settingsChanged()

    def add(self):
        """Add URLs to URLs attr"""
        URLList = re.split(' +/ +', self.newURL)
        for URL in URLList:
            self.URLs.append((
             URL,
             self.encoding,
             self.newAnnotationKey,
             self.newAnnotationValue))

        self.sendButton.settingsChanged()

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            if self.selectedURLLabel:
                cachedLabel = self.selectedURLLabel[0]
            else:
                cachedLabel = None
            del self.URLLabel[:]
            if self.URLs:
                URLs = [ f[0] for f in self.URLs ]
                encodings = [ f[1] for f in self.URLs ]
                annotations = [ '{%s: %s}' % (f[2], f[3]) for f in self.URLs ]
                maxURLLen = max([ len(n) for n in URLs ])
                maxAnnoLen = max([ len(a) for a in annotations ])
                for index in xrange(len(self.URLs)):
                    format = '%-' + unicode(maxURLLen + 2) + 's'
                    URLLabel = format % URLs[index]
                    if maxAnnoLen > 4:
                        if len(annotations[index]) > 4:
                            format = '%-' + unicode(maxAnnoLen + 2) + 's'
                            URLLabel += format % annotations[index]
                        else:
                            URLLabel += ' ' * (maxAnnoLen + 2)
                    URLLabel += encodings[index]
                    self.URLLabel.append(URLLabel)

            self.URLLabel = self.URLLabel
            if cachedLabel is not None:
                self.sendButton.sendIfPreCallback = None
                self.selectedURLLabel.listBox.item(cachedLabel).setSelected(1)
                self.sendButton.sendIfPreCallback = self.updateGUI
            if self.newURL:
                if self.newAnnotationKey and self.newAnnotationValue or not self.newAnnotationKey and not self.newAnnotationValue:
                    self.addButton.setDisabled(False)
                else:
                    self.addButton.setDisabled(True)
            else:
                self.addButton.setDisabled(True)
            if self.autoNumber:
                self.autoNumberKeyLineEdit.setDisabled(False)
            else:
                self.autoNumberKeyLineEdit.setDisabled(True)
            if self.importURLs:
                self.importURLsKeyLineEdit.setDisabled(False)
            else:
                self.importURLsKeyLineEdit.setDisabled(True)
            self.updateURLBoxButtons()
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
        self.adjustSizeWithTimer()
        return

    def updateURLBoxButtons(self):
        """Update state of File box buttons"""
        if self.selectedURLLabel:
            self.removeButton.setDisabled(False)
            if self.selectedURLLabel[0] > 0:
                self.moveUpButton.setDisabled(False)
            else:
                self.moveUpButton.setDisabled(True)
            if self.selectedURLLabel[0] < len(self.URLs) - 1:
                self.moveDownButton.setDisabled(False)
            else:
                self.moveDownButton.setDisabled(True)
        else:
            self.moveUpButton.setDisabled(True)
            self.moveDownButton.setDisabled(True)
            self.removeButton.setDisabled(True)
        if len(self.URLs):
            self.clearAllButton.setDisabled(False)
            self.exportButton.setDisabled(False)
        else:
            self.clearAllButton.setDisabled(True)
            self.exportButton.setDisabled(True)

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def setCaption(self, title):
        if 'captionTitle' in dir(self) and title != 'Orange Widget':
            OWWidget.setCaption(self, title)
            self.sendButton.settingsChanged()
        else:
            OWWidget.setCaption(self, title)

    def onDeleteWidget(self):
        self.clearCreatedInputs()

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
    ow = OWTextableURLs()
    ow.show()
    appl.exec_()
    ow.saveSettings()