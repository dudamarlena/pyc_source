# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableSegment.py
# Compiled at: 2016-07-01 03:18:09
"""
Class OWTextableSegment
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
__version__ = '0.21.4'
import re, codecs, json, LTTL.Segmenter as Segmenter
from LTTL.Segmentation import Segmentation
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableSegment(OWWidget):
    """Orange widget for regex-based tokenization"""
    settingsList = [
     'regexes',
     'importAnnotations',
     'mergeDuplicates',
     'autoSend',
     'autoNumber',
     'autoNumberKey',
     'displayAdvancedSettings',
     'regex',
     'lastLocation',
     'mode',
     'segmentType',
     'uuid']

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Segmentation', Segmentation, self.inputData, Single),
         (
          'Message', JSONMessage, self.inputMessage, Single)]
        self.outputs = [
         (
          'Segmented data', Segmentation)]
        self.regexes = list()
        self.segmentType = 'Segment into words'
        self.importAnnotations = True
        self.mergeDuplicates = False
        self.autoSend = True
        self.autoNumber = False
        self.autoNumberKey = 'num'
        self.displayAdvancedSettings = False
        self.lastLocation = '.'
        self.regex = ''
        self.mode = 'Tokenize'
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.inputSegmentation = None
        self.regexLabels = list()
        self.selectedRegexLabels = list()
        self.newRegex = ''
        self.newAnnotationKey = ''
        self.newAnnotationValue = ''
        self.ignoreCase = False
        self.unicodeDependent = True
        self.multiline = False
        self.dotAll = False
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.updateGUI)
        self.advancedSettings = AdvancedSettings(widget=self.controlArea, master=self, callback=self.sendButton.settingsChanged)
        self.advancedSettings.draw()
        regexBox = OWGUI.widgetBox(widget=self.controlArea, box='Regexes', orientation='vertical')
        regexBoxLine1 = OWGUI.widgetBox(widget=regexBox, box=False, orientation='horizontal', addSpace=True)
        self.regexListbox = OWGUI.listBox(widget=regexBoxLine1, master=self, value='selectedRegexLabels', labels='regexLabels', callback=self.updateRegexBoxButtons, tooltip='The list of regexes that will be applied to each\nsegment of the input segmentation.\n\nRegexes will be applied in the same order as they\nappear in the list.\n\nColumn 1 shows the segmentation mode.\nColumn 2 shows the regex pattern.\nColumn 3 shows the associated annotation (if any).\nColumn 4 shows the associated flags.')
        font = QFont()
        font.setFamily('Courier')
        font.setStyleHint(QFont.Courier)
        font.setPixelSize(12)
        self.regexListbox.setFont(font)
        regexBoxCol2 = OWGUI.widgetBox(widget=regexBoxLine1, orientation='vertical')
        self.moveUpButton = OWGUI.button(widget=regexBoxCol2, master=self, label='Move Up', callback=self.moveUp, tooltip='Move the selected regex upward in the list.')
        self.moveDownButton = OWGUI.button(widget=regexBoxCol2, master=self, label='Move Down', callback=self.moveDown, tooltip='Move the selected regex downward in the list.')
        self.removeButton = OWGUI.button(widget=regexBoxCol2, master=self, label='Remove', callback=self.remove, tooltip='Remove the selected regex from the list.')
        self.clearAllButton = OWGUI.button(widget=regexBoxCol2, master=self, label='Clear All', callback=self.clearAll, tooltip='Remove all regexes from the list.')
        self.exportButton = OWGUI.button(widget=regexBoxCol2, master=self, label='Export List', callback=self.exportList, tooltip='Open a dialog for selecting a file where the\nregex list can be exported in JSON format.')
        self.importButton = OWGUI.button(widget=regexBoxCol2, master=self, label='Import List', callback=self.importList, tooltip='Open a dialog for selecting a regex list to\nimport (in JSON format). Regexes from this list\nwill be added to the existing ones.')
        regexBoxLine2 = OWGUI.widgetBox(widget=regexBox, box=False, orientation='vertical')
        addRegexBox = OWGUI.widgetBox(widget=regexBoxLine2, box=True, orientation='vertical')
        self.modeCombo = OWGUI.comboBox(widget=addRegexBox, master=self, value='mode', sendSelectedValue=True, items=[
         'Tokenize', 'Split'], orientation='horizontal', label='Mode:', labelWidth=131, callback=self.sendButton.settingsChanged, tooltip="Segmentation mode.\n\n'Tokenize': the regex specifies the form of\nsegments themselves.\n\n'Split': the regex specifies the form of\ncharacter sequences occuring between the segments.")
        self.modeCombo.setMinimumWidth(120)
        OWGUI.separator(widget=addRegexBox, height=3)
        OWGUI.lineEdit(widget=addRegexBox, master=self, value='newRegex', orientation='horizontal', label='Regex:', labelWidth=131, callback=self.updateGUI, tooltip='The regex pattern that will be added to the list\nwhen button \'Add\' is clicked. Commonly used\nsegmentation units include:\n1) .\tcharacters (except newline)\n2) \\w\t"letters" (alphanumeric chars and underscores)\n3) \\w+\t"words" (sequences of "letters")\n4) .+\tlines\nand so on.')
        OWGUI.separator(widget=addRegexBox, height=3)
        OWGUI.lineEdit(widget=addRegexBox, master=self, value='newAnnotationKey', orientation='horizontal', label='Annotation key:', labelWidth=131, callback=self.updateGUI, tooltip="This field lets you specify a custom annotation\nkey for segments identified by the regex pattern\nabout to be added to the list.\n\nGroups of characters captured by parentheses in\nthe regex pattern may be inserted in the\nannotation value by using the form '&' (ampersand)\nimmediately followed by a digit indicating the\ncaptured group number (e.g. '&1', '&2', etc.).")
        OWGUI.separator(widget=addRegexBox, height=3)
        OWGUI.lineEdit(widget=addRegexBox, master=self, value='newAnnotationValue', orientation='horizontal', label='Annotation value:', labelWidth=131, callback=self.updateGUI, tooltip="This field lets you specify a custom annotation\nvalue for segments identified by the regex pattern\nabout to be added to the list.\n\nGroups of characters captured by parentheses in\nthe regex pattern may be inserted in the\nannotation value by using the form '&' (ampersand)\nimmediately followed by a digit indicating the\ncaptured group number (e.g. '&1', '&2', etc.).")
        OWGUI.separator(widget=addRegexBox, height=3)
        addRegexBoxLine1 = OWGUI.widgetBox(widget=addRegexBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=addRegexBoxLine1, master=self, value='ignoreCase', label='Ignore case (i)', labelWidth=131, callback=self.updateGUI, tooltip='Regex pattern is case-insensitive.')
        OWGUI.checkBox(widget=addRegexBoxLine1, master=self, value='unicodeDependent', label='Unicode dependent (u)', callback=self.updateGUI, tooltip='Built-in character classes are Unicode-aware.')
        addRegexBoxLine2 = OWGUI.widgetBox(widget=addRegexBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=addRegexBoxLine2, master=self, value='multiline', label='Multiline (m)', labelWidth=131, callback=self.updateGUI, tooltip="Anchors '^' and '$' match the beginning and\nend of each line (rather than just the beginning\nand end of each input segment).")
        OWGUI.checkBox(widget=addRegexBoxLine2, master=self, value='dotAll', label='Dot matches all (s)', callback=self.updateGUI, tooltip="Meta-character '.' matches any character (rather\nthan any character but newline).")
        OWGUI.separator(widget=addRegexBox, height=3)
        self.addButton = OWGUI.button(widget=addRegexBox, master=self, label='Add', callback=self.add, tooltip="Add the regex pattern currently displayed in the\n'Regex' text field to the list.")
        self.advancedSettings.advancedWidgets.append(regexBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        optionsBox = OWGUI.widgetBox(widget=self.controlArea, box='Options', orientation='vertical')
        optionsBoxLine2 = OWGUI.widgetBox(widget=optionsBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=optionsBoxLine2, master=self, value='autoNumber', label='Auto-number with key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Annotate output segments with increasing numeric\nindices.')
        self.autoNumberKeyLineEdit = OWGUI.lineEdit(widget=optionsBoxLine2, master=self, value='autoNumberKey', orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='Annotation key for output segment auto-numbering.')
        OWGUI.separator(widget=optionsBox, height=3)
        OWGUI.checkBox(widget=optionsBox, master=self, value='importAnnotations', label='Import annotations', callback=self.sendButton.settingsChanged, tooltip='Add to each output segment the annotation keys\nand values associated with the corresponding\ninput segment.')
        OWGUI.separator(widget=optionsBox, height=3)
        OWGUI.checkBox(widget=optionsBox, master=self, value='mergeDuplicates', label='Fuse duplicates', callback=self.sendButton.settingsChanged, tooltip='Fuse segments that have the same address.\n\nThe annotation of merged segments will be fused\nas well. In the case where fused segments have\ndistinct values for the same annotation key, only\nthe value of the last one (in order of regex\napplication) will be kept.')
        OWGUI.separator(widget=optionsBox, height=2)
        self.advancedSettings.advancedWidgets.append(optionsBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        basicRegexBox = OWGUI.widgetBox(widget=self.controlArea, box='Segment type', orientation='vertical')
        self.segmentTypeCombo = OWGUI.comboBox(widget=basicRegexBox, master=self, value='segmentType', sendSelectedValue=True, items=[
         'Segment into letters',
         'Segment into words',
         'Segment into lines',
         'Use a regular expression'], orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='Specify the kind of units into which the data will\nbe segmented (letters, words, lines, or custom\nunits defined using a regular expression).')
        self.basicRegexFieldBox = OWGUI.widgetBox(widget=basicRegexBox, box=False, orientation='vertical')
        OWGUI.separator(widget=self.basicRegexFieldBox, height=2)
        OWGUI.lineEdit(widget=self.basicRegexFieldBox, master=self, value='regex', orientation='horizontal', label='Regex:', labelWidth=60, callback=self.sendButton.settingsChanged, tooltip='A pattern that specifies the form of units into\nwhich the data will be segmented.')
        OWGUI.separator(widget=basicRegexBox, height=3)
        self.advancedSettings.basicWidgets.append(basicRegexBox)
        self.advancedSettings.basicWidgetsAppendSeparator()
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def inputMessage(self, message):
        """Handle JSON message on input connection"""
        if not message:
            self.warning(0)
            self.sendButton.settingsChanged()
            return
        else:
            self.displayAdvancedSettings = True
            self.advancedSettings.setVisible(True)
            self.regexes = list()
            self.infoBox.inputChanged()
            try:
                json_data = json.loads(message.content)
                temp_regexes = list()
                for entry in json_data:
                    regex = entry.get('regex', '')
                    annotationKey = entry.get('annotation_key', '')
                    annotationValue = entry.get('annotation_value', '')
                    ignoreCase = entry.get('ignore_case', False)
                    unicodeDependent = entry.get('unicode_dependent', False)
                    multiline = entry.get('multiline', False)
                    dotAll = entry.get('dot_all', False)
                    mode = entry.get('mode', '')
                    if regex == '' or mode == '':
                        self.infoBox.setText('Please verify keys and values of incoming JSON message.', 'error')
                        self.send('Segmented data', None, self)
                        return
                    temp_regexes.append((
                     regex,
                     annotationKey,
                     annotationValue,
                     ignoreCase,
                     unicodeDependent,
                     multiline,
                     dotAll,
                     mode))

                self.regexes.extend(temp_regexes)
                self.sendButton.settingsChanged()
            except ValueError:
                self.infoBox.setText('Please make sure that incoming message is valid JSON.', 'error')
                self.send('Segmented data', None, self)
                return

            return

    def sendData(self):
        """(Have LTTL.Segmenter) perform the actual tokenization"""
        if not self.inputSegmentation:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Segmented data', None, self)
            return
        else:
            if self.displayAdvancedSettings and not self.regexes or self.segmentType == 'Use a regular expression' and not (self.regex or self.displayAdvancedSettings):
                self.infoBox.setText('Please enter a regex.', 'warning')
                self.send('Segmented data', None, self)
                return
            regexForType = {'Segment into letters': '\\w', 
               'Segment into words': '\\w+', 
               'Segment into lines': '.+'}
            if self.displayAdvancedSettings:
                myRegexes = self.regexes
            else:
                if self.segmentType == 'Use a regular expression':
                    myRegexes = [
                     [
                      self.regex,
                      None,
                      None,
                      False,
                      True,
                      False,
                      False,
                      'tokenize']]
                else:
                    myRegexes = [
                     [
                      regexForType[self.segmentType],
                      None,
                      None,
                      False,
                      True,
                      False,
                      False,
                      'tokenize']]
                if self.displayAdvancedSettings:
                    importAnnotations = self.importAnnotations
                    if self.autoNumber:
                        autoNumberKey = self.autoNumberKey
                        if autoNumberKey == '':
                            self.infoBox.setText('Please enter an annotation key for auto-numbering.', 'warning')
                            self.send('Segmented data', None, self)
                            return
                    else:
                        autoNumberKey = None
                    mergeDuplicates = self.mergeDuplicates
                else:
                    importAnnotations = True
                    autoNumberKey = None
                    mergeDuplicates = False
                regexes = list()
                for regex_idx in xrange(len(myRegexes)):
                    regex = myRegexes[regex_idx]
                    regex_string = regex[0]
                    if regex[3] or regex[4] or regex[5] or regex[6]:
                        flags = ''
                        if regex[3]:
                            flags += 'i'
                        if regex[4]:
                            flags += 'u'
                        if regex[5]:
                            flags += 'm'
                        if regex[6]:
                            flags += 's'
                        regex_string += '(?%s)' % flags
                    try:
                        if regex[1] and regex[2]:
                            regexes.append((
                             re.compile(regex_string),
                             regex[7].lower(), {regex[1]: regex[2]}))
                        else:
                            regexes.append((re.compile(regex_string), regex[7].lower()))
                    except re.error as re_error:
                        message = 'Please enter a valid regex (error: %s' % re_error.message
                        if self.displayAdvancedSettings and len(myRegexes) > 1:
                            message += ', regex #%i' % (regex_idx + 1)
                        message += ').'
                        self.infoBox.setText(message, 'error')
                        self.send('Segmented data', None, self)
                        return

                progressBar = OWGUI.ProgressBar(self, iterations=len(self.inputSegmentation) * len(myRegexes))
                self.warning(0)
                self.error(0)
                try:
                    segmented_data = Segmenter.tokenize(segmentation=self.inputSegmentation, regexes=regexes, label=self.captionTitle, import_annotations=importAnnotations, merge_duplicates=mergeDuplicates, auto_number_as=autoNumberKey, progress_callback=progressBar.advance)
                    message = '%i segment@p sent to output.' % len(segmented_data)
                    message = pluralize(message, len(segmented_data))
                    self.infoBox.setText(message)
                    self.send('Segmented data', segmented_data, self)
                except IndexError:
                    self.infoBox.setText('reference to unmatched group in annotation key and/or value.', 'error')
                    self.send('Segmented data', None, self)

            self.sendButton.resetSettingsChangedFlag()
            progressBar.finish()
            return

    def inputData(self, segmentation):
        """Process incoming segmentation"""
        self.inputSegmentation = segmentation
        self.infoBox.inputChanged()
        self.sendButton.sendIf()

    def importList(self):
        """Display a FileDialog and import regex list"""
        filePath = unicode(QFileDialog.getOpenFileName(self, 'Import Regex List', self.lastLocation, 'Text files (*)'))
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
                temp_regexes = list()
                for entry in json_data:
                    regex = entry.get('regex', '')
                    annotationKey = entry.get('annotation_key', '')
                    annotationValue = entry.get('annotation_value', '')
                    ignoreCase = entry.get('ignore_case', False)
                    unicodeDependent = entry.get('unicode_dependent', False)
                    multiline = entry.get('multiline', False)
                    dotAll = entry.get('dot_all', False)
                    mode = entry.get('mode', '')
                    if regex == '' or mode == '':
                        QMessageBox.warning(None, 'Textable', "Selected JSON file doesn't have the right keys and/or values.", QMessageBox.Ok)
                        return
                    temp_regexes.append((
                     regex,
                     annotationKey,
                     annotationValue,
                     ignoreCase,
                     unicodeDependent,
                     multiline,
                     dotAll,
                     mode))

                self.regexes.extend(temp_regexes)
                if temp_regexes:
                    self.sendButton.settingsChanged()
            except ValueError:
                QMessageBox.warning(None, 'Textable', 'Selected file is not in JSON format.', QMessageBox.Ok)
                return

            return

    def exportList(self):
        """Display a FileDialog and export regex list"""
        toDump = list()
        for regex in self.regexes:
            toDump.append({'regex': regex[0], 
               'mode': regex[7]})
            if regex[1] and regex[2]:
                toDump[(-1)]['annotation_key'] = regex[1]
                toDump[(-1)]['annotation_value'] = regex[2]
            if regex[3]:
                toDump[(-1)]['ignore_case'] = regex[3]
            if regex[4]:
                toDump[(-1)]['unicode_dependent'] = regex[4]
            if regex[5]:
                toDump[(-1)]['multiline'] = regex[5]
            if regex[6]:
                toDump[(-1)]['dot_all'] = regex[6]

        filePath = unicode(QFileDialog.getSaveFileName(self, 'Export Regex List', self.lastLocation))
        if filePath:
            self.lastLocation = os.path.dirname(filePath)
            outputFile = codecs.open(filePath, encoding='utf8', mode='w', errors='xmlcharrefreplace')
            outputFile.write(normalizeCarriageReturns(json.dumps(toDump, sort_keys=True, indent=4)))
            outputFile.close()
            QMessageBox.information(None, 'Textable', 'Regex list correctly exported', QMessageBox.Ok)
        return

    def moveUp(self):
        """Move regex upward in Regexes listbox"""
        if self.selectedRegexLabels:
            index = self.selectedRegexLabels[0]
            if index > 0:
                temp = self.regexes[(index - 1)]
                self.regexes[index - 1] = self.regexes[index]
                self.regexes[index] = temp
                self.selectedRegexLabels.listBox.item(index - 1).setSelected(1)
                self.sendButton.settingsChanged()

    def moveDown(self):
        """Move regex downward in Regexes listbox"""
        if self.selectedRegexLabels:
            index = self.selectedRegexLabels[0]
            if index < len(self.regexes) - 1:
                temp = self.regexes[(index + 1)]
                self.regexes[index + 1] = self.regexes[index]
                self.regexes[index] = temp
                self.selectedRegexLabels.listBox.item(index + 1).setSelected(1)
                self.sendButton.settingsChanged()

    def clearAll(self):
        """Remove all regexes from Regexes"""
        del self.regexes[:]
        del self.selectedRegexLabels[:]
        self.sendButton.settingsChanged()

    def remove(self):
        """Remove regex from regexes attr"""
        if self.selectedRegexLabels:
            index = self.selectedRegexLabels[0]
            self.regexes.pop(index)
            del self.selectedRegexLabels[:]
            self.sendButton.settingsChanged()

    def add(self):
        """Add regex to regexes attr"""
        self.regexes.append((
         self.newRegex,
         self.newAnnotationKey,
         self.newAnnotationValue,
         self.ignoreCase,
         self.unicodeDependent,
         self.multiline,
         self.dotAll,
         self.mode))
        self.sendButton.settingsChanged()

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            if self.selectedRegexLabels:
                cachedLabel = self.selectedRegexLabels[0]
            else:
                cachedLabel = None
            del self.regexLabels[:]
            if len(self.regexes):
                regexes = [ r[0] for r in self.regexes ]
                annotations = [ '{%s: %s}' % (r[1], r[2]) for r in self.regexes ]
                maxRegexLen = max([ len(r) for r in regexes ])
                maxAnnoLen = max([ len(a) for a in annotations ])
                for index in range(len(self.regexes)):
                    regexLabel = '(%s)  ' % self.regexes[index][7][0].lower()
                    format = '%-' + unicode(maxRegexLen + 2) + 's'
                    regexLabel += format % regexes[index]
                    if maxAnnoLen > 4:
                        if len(annotations[index]) > 4:
                            format = '%-' + unicode(maxAnnoLen + 2) + 's'
                            regexLabel += format % annotations[index]
                        else:
                            regexLabel += ' ' * (maxAnnoLen + 2)
                    flags = list()
                    if self.regexes[index][3]:
                        flags.append('i')
                    if self.regexes[index][4]:
                        flags.append('u')
                    if self.regexes[index][5]:
                        flags.append('m')
                    if self.regexes[index][6]:
                        flags.append('s')
                    if len(flags):
                        regexLabel += '[%s]' % (',').join(flags)
                    self.regexLabels.append(regexLabel)

            self.regexLabels = self.regexLabels
            if cachedLabel is not None:
                self.sendButton.sendIfPreCallback = None
                self.selectedRegexLabels.listBox.item(cachedLabel).setSelected(1)
                self.sendButton.sendIfPreCallback = self.updateGUI
            if self.newRegex:
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
            self.updateRegexBoxButtons()
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            self.basicRegexFieldBox.setVisible(self.segmentType == 'Use a regular expression')
        self.adjustSizeWithTimer()
        return

    def updateRegexBoxButtons(self):
        """Update state of Regex box buttons"""
        if self.selectedRegexLabels:
            self.removeButton.setDisabled(False)
            if self.selectedRegexLabels[0] > 0:
                self.moveUpButton.setDisabled(False)
            else:
                self.moveUpButton.setDisabled(True)
            if self.selectedRegexLabels[0] < len(self.regexes) - 1:
                self.moveDownButton.setDisabled(False)
            else:
                self.moveDownButton.setDisabled(True)
        else:
            self.moveUpButton.setDisabled(True)
            self.moveDownButton.setDisabled(True)
            self.removeButton.setDisabled(True)
        if self.regexes:
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
    from LTTL.Input import Input
    appl = QApplication(sys.argv)
    ow = OWTextableSegment()
    ow.inputData(Input('a simple example'))
    ow.show()
    appl.exec_()
    ow.saveSettings()