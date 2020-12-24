# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableCategory.py
# Compiled at: 2016-08-11 10:06:54
"""
Class OWTextableCategory
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
__version__ = '0.12.3'
from LTTL.Table import Table
from LTTL.Segmentation import Segmentation
import LTTL.Processor as Processor
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableCategory(OWWidget):
    """Orange widget for extracting content or annotation information"""
    contextHandlers = {'': SegmentationListContextHandler('', [
          ContextInputListField('segmentations'),
          ContextInputIndex('units'),
          ContextInputIndex('_contexts'),
          'unitAnnotationKey',
          'contextAnnotationKey',
          'sequenceLength',
          'uuid'])}
    settingsList = [
     'autoSend',
     'intraSeqDelim',
     'sortOrder',
     'sortReverse',
     'keepOnlyFirst',
     'valueDelimiter',
     'sequenceLength']

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Category widget"""
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Segmentation', Segmentation, self.inputData, Multiple)]
        self.outputs = [
         (
          'Textable table', Table, Default),
         (
          'Orange table', Orange.data.Table)]
        self.autoSend = False
        self.sequenceLength = 1
        self.intraSeqDelim = '#'
        self.sortOrder = 'Frequency'
        self.sortReverse = True
        self.keepOnlyFirst = True
        self.valueDelimiter = '|'
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentations = list()
        self.units = None
        self.unitAnnotationKey = None
        self._contexts = None
        self.contextAnnotationKey = None
        self.settingsRestored = False
        self.infoBox = InfoBox(widget=self.controlArea, stringClickSend=", please click 'Send' when ready.")
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', buttonLabel='Send', checkboxLabel='Send automatically', sendIfPreCallback=self.updateGUI)
        self.unitsBox = OWGUI.widgetBox(widget=self.controlArea, box='Units', orientation='vertical', addSpace=True)
        self.unitSegmentationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='units', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segments will be used for\ndetermining categories.')
        self.unitSegmentationCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.unitAnnotationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='unitAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether categories are defined by the\nsegments' content (value 'none') or by their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.sequenceLengthSpin = OWGUI.spin(widget=self.unitsBox, master=self, value='sequenceLength', min=1, max=1, step=1, orientation='horizontal', label='Sequence length:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Indicate whether to use single segments or rather\nsequences of 2, 3, ... segments (n-grams) for\ncategory extraction.')
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.intraSeqDelimLineEdit = OWGUI.lineEdit(widget=self.unitsBox, master=self, value='intraSeqDelim', orientation='horizontal', label='Intra-sequence delimiter:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="If 'Sequence length' above is set to a value\nlarger than 1, the (possibly empty) string\nspecified in this field will be used as a\ndelimiter between the successive segments of\neach sequence.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.multipleValuesBox = OWGUI.widgetBox(widget=self.controlArea, box='Multiple Values', orientation='vertical', addSpace=True)
        self.sortOrderCombo = OWGUI.comboBox(widget=self.multipleValuesBox, master=self, value='sortOrder', items=[
         'Frequency', 'ASCII'], sendSelectedValue=True, orientation='horizontal', label='Sort by:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Criterion for sorting multiple categories.')
        self.sortOrderCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.multipleValuesBox, height=3)
        self.sortReverseCheckBox = OWGUI.checkBox(widget=self.multipleValuesBox, master=self, value='sortReverse', label='Sort in reverse order', callback=self.sendButton.settingsChanged, tooltip='Sort in reverse (i.e. decreasing) order.')
        OWGUI.separator(widget=self.multipleValuesBox, height=3)
        OWGUI.checkBox(widget=self.multipleValuesBox, master=self, value='keepOnlyFirst', label='Keep only first value', callback=self.sendButton.settingsChanged, tooltip='Keep only the first category\n(after sorting).')
        OWGUI.separator(widget=self.multipleValuesBox, height=3)
        self.multipleValuesDelimLineEdit = OWGUI.lineEdit(widget=self.multipleValuesBox, master=self, value='valueDelimiter', orientation='horizontal', label='Value delimiter:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="If 'Keep only first value' above is unchecked\nand there are multiple categories, the (possibly\nempty) string specified in this field will be\nused as a delimiter between them.")
        OWGUI.separator(widget=self.multipleValuesBox, height=3)
        self.contextsBox = OWGUI.widgetBox(widget=self.controlArea, box='Contexts', orientation='vertical', addSpace=True)
        self.contextSegmentationCombo = OWGUI.comboBox(widget=self.contextsBox, master=self, value='_contexts', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segment types define\nthe contexts to which categories will be\nassigned.')
        OWGUI.separator(widget=self.contextsBox, height=3)
        self.contextAnnotationCombo = OWGUI.comboBox(widget=self.contextsBox, master=self, value='contextAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether context types are defined by\nthe content of segments in the above specified\nsegmentation (value 'none') or by their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=self.contextsBox, height=3)
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
        if index == self._contexts:
            self.mode = 'No context'
            self._contexts = None
        elif index < self._contexts:
            self._contexts -= 1
            if self._contexts < 0:
                self.mode = 'No context'
                self._contexts = None
        return

    def sendData(self):
        """Check input, build table, then send it"""
        if len(self.segmentations) == 0:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Textable table', None)
            self.send('Orange table', None)
            return
        else:
            units = {'segmentation': self.segmentations[self.units][1], 
               'annotation_key': self.unitAnnotationKey or None, 
               'seq_length': self.sequenceLength, 
               'intra_seq_delimiter': self.intraSeqDelim}
            if units['annotation_key'] == '(none)':
                units['annotation_key'] = None
            multipleValues = {'sort_order': self.sortOrder, 
               'reverse': self.sortReverse, 
               'keep_only_first': self.keepOnlyFirst, 
               'value_delimiter': self.valueDelimiter}
            contexts = {'segmentation': self.segmentations[self._contexts][1], 
               'annotation_key': self.contextAnnotationKey or None}
            if contexts['annotation_key'] == '(none)':
                contexts['annotation_key'] = None
            progressBar = OWGUI.ProgressBar(self, iterations=len(contexts['segmentation']))
            table = Processor.annotate_contexts(units, multipleValues, contexts, progress_callback=progressBar.advance)
            progressBar.finish()
            if not len(table.row_ids):
                self.infoBox.setText('Resulting table is empty.', 'warning')
                self.send('Textable table', None)
                self.send('Orange table', None)
            else:
                self.infoBox.setText('Table sent to output.')
                self.send('Textable table', table)
                self.send('Orange table', table.to_orange_table())
            self.sendButton.resetSettingsChangedFlag()
            return

    def updateGUI(self):
        """Update GUI state"""
        self.unitSegmentationCombo.clear()
        self.unitAnnotationCombo.clear()
        self.unitAnnotationCombo.addItem('(none)')
        if len(self.segmentations) == 0:
            self.units = None
            self.unitAnnotationKey = ''
            self.unitsBox.setDisabled(True)
            self.contextsBox.setDisabled(True)
            self.adjustSize()
            return
        else:
            if len(self.segmentations) == 1:
                self.units = 0
            for segmentation in self.segmentations:
                self.unitSegmentationCombo.addItem(segmentation[1].label)

            self.units = self.units
            unitAnnotationKeys = self.segmentations[self.units][1].get_annotation_keys()
            for k in unitAnnotationKeys:
                self.unitAnnotationCombo.addItem(k)

            if self.unitAnnotationKey not in unitAnnotationKeys:
                self.unitAnnotationKey = '(none)'
            self.unitAnnotationKey = self.unitAnnotationKey
            self.unitsBox.setDisabled(False)
            self.sequenceLengthSpin.control.setRange(1, len(self.segmentations[self.units][1]))
            self.sequenceLength = self.sequenceLength or 1
            self.contextsBox.setDisabled(False)
            self.contextSegmentationCombo.clear()
            for index in range(len(self.segmentations)):
                self.contextSegmentationCombo.addItem(self.segmentations[index][1].label)

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
            self.adjustSizeWithTimer()
            return

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def handleNewSignals(self):
        """Overridden: called after multiple signals have been added"""
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
    from LTTL.Input import Input
    from LTTL.Segmenter import Segmenter
    import re
    appl = QApplication(sys.argv)
    ow = OWTextableCategory()
    seg1 = Input('aaabc', 'text1')
    seg2 = Input('abbc', 'text2')
    segmenter = Segmenter()
    seg3 = segmenter.concatenate([
     seg1, seg2], import_labels_as='string', label='corpus')
    seg4 = segmenter.tokenize(seg3, regexes=[
     (
      re.compile('\\w+'), 'Tokenize')])
    seg5 = segmenter.tokenize(seg4, regexes=[
     (
      re.compile('[ai]'), 'Tokenize')], label='V')
    seg6 = segmenter.tokenize(seg4, regexes=[
     (
      re.compile('[bc]'), 'Tokenize')], label='C')
    seg7 = segmenter.concatenate([
     seg5, seg6], import_labels_as='category', label='letters', sort=True, merge_duplicates=True)
    ow.inputData(seg7, 1)
    ow.inputData(seg4, 2)
    ow.show()
    appl.exec_()
    ow.saveSettings()