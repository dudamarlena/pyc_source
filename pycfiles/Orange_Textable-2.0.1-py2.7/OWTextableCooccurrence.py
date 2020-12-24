# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableCooccurrence.py
# Compiled at: 2016-08-11 10:17:33
"""
Class OWTextableCooccurrence
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
__version__ = '1.0.1'
__author__ = 'Mahtab Mohammadi'
__maintainer__ = 'LangTech Sarl'
import LTTL.Processor as Processor
from LTTL.Table import IntPivotCrosstab
from LTTL.Segmentation import Segmentation
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI, re

class OWTextableCooccurrence(OWWidget):
    """Orange widget for calculating co-occurrences of text units"""
    contextHandlers = {'': SegmentationListContextHandler('', [
          ContextInputListField('segmentations'),
          ContextInputIndex('units'),
          ContextInputIndex('_contexts'),
          ContextInputIndex('units2'),
          'mode',
          'unitAnnotationKey',
          'unit2AnnotationKey',
          'contextAnnotationKey',
          'coocWithUnits2sequenceLength',
          'windowSize',
          'uuid'])}
    settingsList = [
     'autoSend',
     'intraSeqDelim',
     'sequenceLength',
     'windowSize',
     'coocWithUnits2']

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Cooccurrence widget"""
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Segmentation', Segmentation, self.inputData, Multiple)]
        self.outputs = [
         (
          'Textable pivot crosstab', IntPivotCrosstab, Default),
         (
          'Orange table', Orange.data.Table)]
        self.autoSend = False
        self.sequenceLength = 1
        self.intraSeqDelim = '#'
        self.mode = 'Sliding window'
        self.coocWithUnits2 = False
        self.windowSize = 2
        self.units = None
        self.unitAnnotationKey = None
        self.units2 = None
        self.unit2AnnotationKey = None
        self._contexts = None
        self.contextAnnotationKey = None
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentations = list()
        self.infoBox = InfoBox(widget=self.controlArea, stringClickSend=", please click 'Send' when ready.")
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', buttonLabel='Send', checkboxLabel='Send automatically', sendIfPreCallback=self.updateGUI)
        self.unitsBox = OWGUI.widgetBox(widget=self.controlArea, box='Units', orientation='vertical', addSpace=True)
        self.unitsegmentationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='units', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation for which the co-occurrences of\nsegments will be counted.\nThis defines the columns of the resulting crosstab,\nas well as its rows if no secondary units are being used.')
        self.unitsegmentationCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.unitAnnotationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='unitAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicates whether the items whose co-occurrences will be\ncounted in the above specified segmentation\nare defined by the segments' content (value 'none')\nor by their annotation values for a specific\nannotation key.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.sequenceLengthSpin = OWGUI.spin(widget=self.unitsBox, master=self, value='sequenceLength', min=1, max=1, step=1, orientation='horizontal', label='Sequence length:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Indicates whether to count the co-occurrences of\nsingle segments or rather of sequences of 2,\n3, ... segments (n-grams).\n\nNote that this parameter cannot be set to a\nvalue larger than 1 if co-occurrences are to be\ncounted between primary and secondary units.')
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.intraSeqDelimLineEdit = OWGUI.lineEdit(widget=self.unitsBox, master=self, value='intraSeqDelim', orientation='horizontal', label='Intra-sequence delimiter:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="If 'Sequence length' above is set to a value\nlarger than 1, the (possibly empty) string\nspecified in this field will be used as a\ndelimiter between the successive segments of\neach sequence.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.units2Box = OWGUI.widgetBox(widget=self.controlArea, box='Secondary units', orientation='vertical', addSpace=True)
        self.coocWithUnits2Checkbox = OWGUI.checkBox(widget=self.units2Box, master=self, value='coocWithUnits2', label='Use secondary units', callback=self.sendButton.settingsChanged, tooltip='Check this box to count the co-occurrences of\nprimary and secondary units.')
        OWGUI.separator(widget=self.units2Box, height=3)
        iBox = OWGUI.indentedBox(widget=self.units2Box)
        self.unit2SegmentationCombo = OWGUI.comboBox(widget=iBox, master=self, value='units2', emptyString='(none)', orientation='horizontal', label='Segmentation:', labelWidth=160, callback=self.sendButton.settingsChanged, tooltip='The segmentation for which the co-occurrences of\nsegments will be counted with respect to primary units\nThis defines the rows of the resulting crosstab, and\ntherefore the primary units define only the columns of the\nresulting crosstab.')
        OWGUI.separator(widget=iBox, height=3)
        self.unit2AnnotationCombo = OWGUI.comboBox(widget=iBox, master=self, value='unit2AnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=160, callback=self.sendButton.settingsChanged, tooltip="Indicate whether the items of the secondary unit\nsegmentation whose co-occurrences will be counted\nare defined by the segments' content (value 'none')\nor by their annotation values for a specific\nannotation key.")
        self.coocWithUnits2Checkbox.disables.append(iBox)
        if self.coocWithUnits2:
            iBox.setDisabled(False)
        else:
            iBox.setDisabled(True)
        OWGUI.separator(widget=self.units2Box, height=3)
        self._contextsBox = OWGUI.widgetBox(widget=self.controlArea, box='Contexts', orientation='vertical', addSpace=True)
        self.modeCombo = OWGUI.comboBox(widget=self._contextsBox, master=self, value='mode', sendSelectedValue=True, items=[
         'Sliding window',
         'Containing segmentation'], orientation='horizontal', label='Mode', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Context specification mode.\n\n'Sliding window': contexts are defined as all the\nsuccessive, overlapping sequences of n segments\nin the 'units' segmentation.\n\n'Containing segmentation': contexts are defined\nas the distinct segments occurring in a given\nsegmentation.\n")
        self.slidingWindowBox = OWGUI.widgetBox(widget=self._contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.slidingWindowBox, height=3)
        self.windowSizeSpin = OWGUI.spin(widget=self.slidingWindowBox, master=self, value='windowSize', min=2, max=2, step=1, orientation='horizontal', label='Window size:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The length of segment sequences defining contexts.')
        self.containingSegmentationBox = OWGUI.widgetBox(widget=self._contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextSegmentationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='_contexts', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segment types define\nthe contexts in which co-occurrences will be counted.')
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextAnnotationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='contextAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicates whether context types are defined by\nthe content of segments in the above specified\nsegmentation (value 'none') or by their annotation\nvalues for a specific annotation key.")
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def inputData(self, newItem, newId=None):
        """Process incoming data."""
        self.closeContext()
        updateMultipleInputs(self.segmentations, newItem, newId, self.onInputRemoval)
        self.infoBox.inputChanged()
        self.updateGUI()

    def onInputRemoval(self, index):
        """Handle removal of input with given index"""
        if index < self.units:
            self.units -= 1
        elif index == self.units and self.units == len(self.segmentations) - 1:
            self.units -= 1
            if self.units < 0:
                self.units = None
        if index < self.units2:
            self.units2 -= 1
        elif index == self.units2 and self.units2 == len(self.segmentations) - 1:
            self.units2 -= 1
            if self.units2 < 0:
                self.units2 = None
        if self.mode == 'Containing segmentation':
            if index < self._contexts:
                self._contexts -= 1
            elif index == self._contexts:
                if self._contexts == len(self.segmentations) - 1:
                    self._contexts -= 1
                    if self._contexts < 0:
                        self._contexts = None
                if self.autoSend:
                    self.autoSend = False
                self.infoBox.setText("The selected context segmentation has been removed.\n'Send automatically' checkbox will be unchecked.\nPlease connect a segmentation to the widget and\ntry again.", state='warning')
                self.send('Textable pivot crosstab', None)
                self.send('Orange table', None)
        return

    def sendData(self):
        """Check input, compute co-occurrence, then send tabel"""
        if len(self.segmentations) == 0:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Textable pivot crosstab', None)
            self.send('Orange table', None)
            return
        else:
            units = {'segmentation': self.segmentations[self.units][1], 
               'annotation_key': self.unitAnnotationKey or None, 
               'seq_length': self.sequenceLength, 
               'intra_seq_delimiter': self.intraSeqDelim}
            if units['annotation_key'] == '(none)':
                units['annotation_key'] = None
            if self.mode == 'Sliding window':
                progressBar = OWGUI.ProgressBar(self, iterations=len(units['segmentation']) - (self.windowSize - 1))
                table = Processor.cooc_in_window(units, window_size=self.windowSize, progress_callback=progressBar.advance)
                progressBar.finish()
            elif self.mode == 'Containing segmentation':
                contexts = {'segmentation': self.segmentations[self._contexts][1], 'annotation_key': self.contextAnnotationKey or None}
                if contexts['annotation_key'] == '(none)':
                    contexts['annotation_key'] = None
                if self.units2 is not None and self.coocWithUnits2:
                    units2 = {'segmentation': self.segmentations[self.units2][1], 
                       'annotation_key': self.unit2AnnotationKey or None}
                    if units2['annotation_key'] == '(none)':
                        units2['annotation_key'] = None
                    num_iterations = len(contexts['segmentation'])
                    progressBar = OWGUI.ProgressBar(self, iterations=num_iterations * 2)
                    table = Processor.cooc_in_context(units, contexts, units2, progress_callback=progressBar.advance)
                else:
                    num_iterations = len(contexts['segmentation'])
                    progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
                    table = Processor.cooc_in_context(units, contexts, progress_callback=progressBar.advance)
                progressBar.finish()
            if len(table.row_ids) == 0:
                self.infoBox.setText('Resulting table is empty.', 'warning')
                self.send('Textable pivot crosstab', None)
                self.send('Orange table', None)
            else:
                total = sum([ i for i in table.values.values() ])
                message = 'Table with %i cooccurrence@p sent to output.' % total
                message = pluralize(message, total)
                self.infoBox.setText(message)
                self.send('Textable pivot crosstab', table)
                self.send('Orange table', table.to_orange_table())
            self.sendButton.resetSettingsChangedFlag()
            return

    def updateGUI(self):
        """Update GUI state"""
        self.unitsegmentationCombo.clear()
        self.unitAnnotationCombo.clear()
        self.unitAnnotationCombo.addItem('(none)')
        self.unit2SegmentationCombo.clear()
        self.unit2AnnotationCombo.clear()
        self.unit2AnnotationCombo.addItem('(none)')
        if len(self.segmentations) == 0:
            self.units = None
            self.unitAnnotationKey = ''
            self.unitsBox.setDisabled(True)
            self.units2 = None
            self.unit2AnnotationKey = ''
            self.units2Box.setDisabled(True)
            self.mode = 'Sliding window'
            self._contextsBox.setDisabled(True)
            self.adjustSize()
            return
        else:
            if len(self.segmentations) == 1:
                self.units = 0
            for segmentation in self.segmentations:
                try:
                    self.unitsegmentationCombo.addItem(segmentation[1].label)
                except TypeError:
                    self.unitsBox.setDisabled(True)

            self.units = self.units
            unitAnnotationKeys = self.segmentations[self.units][1].get_annotation_keys()
            for k in unitAnnotationKeys:
                self.unitAnnotationCombo.addItem(k)

            if self.unitAnnotationKey not in unitAnnotationKeys:
                self.unitAnnotationKey = '(none)'
            self.unitAnnotationKey = self.unitAnnotationKey
            self.unitsBox.setDisabled(False)
            self.sequenceLengthSpin.control.setRange(1, len(self.segmentations[self.units][1]))
            self.sequenceLength = self.sequenceLength
            if self.sequenceLength > 1:
                self.units2Box.setDisabled(True)
            else:
                self.units2Box.setDisabled(False)
            self._contextsBox.setDisabled(False)
            if self.mode == 'Sliding window':
                self.units2 = None
                self.units2Box.setDisabled(True)
                self.containingSegmentationBox.setVisible(False)
                self.slidingWindowBox.setVisible(True)
                self.sequenceLengthSpin.setDisabled(False)
                self.windowSizeSpin.control.setRange(2, len(self.segmentations[self.units][1]))
                self.windowSize = self.windowSize
            elif self.mode == 'Containing segmentation':
                if len(self.segmentations) == 1:
                    self.units2 = None
                    self.unit2AnnotationKey = ''
                    self.units2Box.setDisabled(True)
                else:
                    if len(self.segmentations) >= 2:
                        self.units2Box.setDisabled(False)
                    self.slidingWindowBox.setVisible(False)
                    self.containingSegmentationBox.setVisible(True)
                    self.contextSegmentationCombo.clear()
                    try:
                        for index in range(len(self.segmentations)):
                            self.contextSegmentationCombo.addItem(self.segmentations[index][1].label)

                    except TypeError:
                        self._contextsBox.setDisabled(True)

                    self._contexts = self._contexts or 0
                    segmentation = self.segmentations[self._contexts]
                    self.contextAnnotationCombo.clear()
                    self.contextAnnotationCombo.addItem('(none)')
                    contextAnnotationKeys = segmentation[1].get_annotation_keys()
                    for key in contextAnnotationKeys:
                        self.contextAnnotationCombo.addItem(key)

                if self.contextAnnotationKey not in contextAnnotationKeys:
                    self.contextAnnotationKey = '(none)'
                self.contextAnnotationKey = self.contextAnnotationKey
                if self.coocWithUnits2:
                    try:
                        for segmentation in self.segmentations:
                            self.unit2SegmentationCombo.addItem(segmentation[1].label)

                    except TypeError:
                        self.units2Box.setDisabled(True)

                    self.units2 = self.units2 or 0
                    unit2AnnotationKeys = self.segmentations[self.units2][1].get_annotation_keys()
                    for k in unit2AnnotationKeys:
                        self.unit2AnnotationCombo.addItem(k)

                    if self.unit2AnnotationKey not in unit2AnnotationKeys:
                        self.unit2AnnotationKey = '(none)'
                    self.unit2AnnotationKey = self.unit2AnnotationKey
                    self.sequenceLength = 1
                    self.sequenceLengthSpin.setDisabled(True)
            self.adjustSizeWithTimer()
            return

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def handleNewSignals(self):
        """Overridden: called after multiple singnals have been added"""
        self.openContext('', self.segmentations)
        self.updateGUI()
        self.sendButton.sendIf()

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
    import LTTL.Segmenter as Segmenter
    from LTTL.Input import Input
    appl = QApplication(sys.argv)
    ow = OWTextableCooccurrence()
    seg1 = Input('un texte', label='text')
    seg2 = Segmenter.tokenize(seg1, regexes=[
     (
      re.compile('\\w+'),
      'tokenize', {'type': 'W'})], label='words')
    seg3 = Segmenter.tokenize(seg1, regexes=[
     (
      re.compile('[aeiouy]'),
      'tokenize', {'type': 'V'})], label='vowel')
    seg4 = Segmenter.tokenize(seg1, regexes=[
     (
      re.compile('[^aeiouy]'),
      'tokenize', {'type2': 'C'})], label='consonant')
    ow.inputData(seg3, 1)
    ow.inputData(seg2, 2)
    ow.inputData(seg4, 3)
    ow.show()
    appl.exec_()
    ow.saveSettings()