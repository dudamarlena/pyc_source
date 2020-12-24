# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableCount.py
# Compiled at: 2016-08-18 08:22:44
"""
Class OWTextableCount
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
__version__ = '0.21.5'
from LTTL.Table import IntPivotCrosstab
from LTTL.Segmentation import Segmentation
import LTTL.Processor as Processor
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableCount(OWWidget):
    """Orange widget for counting text units"""
    contextHandlers = {'': SegmentationListContextHandler('', [
          ContextInputListField('segmentations'),
          ContextInputIndex('units'),
          ContextInputIndex('_contexts'),
          'mode',
          'unitAnnotationKey',
          'contextAnnotationKey',
          'sequenceLength',
          'windowSize',
          'leftContextSize',
          'rightContextSize',
          'uuid'])}
    settingsList = [
     'autoSend',
     'intraSeqDelim',
     'unitPosMarker',
     'mergeContexts',
     'sequenceLength',
     'windowSize',
     'leftContextSize',
     'rightContextSize',
     'mergeStrings']

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Count widget"""
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
        self.mode = 'No context'
        self.mergeContexts = False
        self.windowSize = 1
        self.leftContextSize = 0
        self.rightContextSize = 0
        self.mergeStrings = False
        self.unitPosMarker = '_'
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentations = list()
        self.units = None
        self.unitAnnotationKey = None
        self._contexts = None
        self.contextAnnotationKey = None
        self.infoBox = InfoBox(widget=self.controlArea, stringClickSend=", please click 'Send' when ready.")
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', buttonLabel='Send', checkboxLabel='Send automatically', sendIfPreCallback=self.updateGUI)
        self.unitsBox = OWGUI.widgetBox(widget=self.controlArea, box='Units', orientation='vertical', addSpace=True)
        self.unitSegmentationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='units', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segments will be counted.\nThis defines the columns of the resulting crosstab.')
        self.unitSegmentationCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.unitAnnotationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='unitAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether the items to be counted in the\nabove specified segmentation are defined by the\nsegments' content (value 'none') or by their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.sequenceLengthSpin = OWGUI.spin(widget=self.unitsBox, master=self, value='sequenceLength', min=1, max=1, step=1, orientation='horizontal', label='Sequence length:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Indicate whether to count single segments or\nrather sequences of 2, 3, ... segments (n-grams).')
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.intraSeqDelimLineEdit = OWGUI.lineEdit(widget=self.unitsBox, master=self, value='intraSeqDelim', orientation='horizontal', label='Intra-sequence delimiter:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="If 'Sequence length' above is set to a value\nlarger than 1, the (possibly empty) string\nspecified in this field will be used as a\ndelimiter between the successive segments of\neach sequence.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.contextsBox = OWGUI.widgetBox(widget=self.controlArea, box='Contexts', orientation='vertical', addSpace=True)
        self.modeCombo = OWGUI.comboBox(widget=self.contextsBox, master=self, value='mode', sendSelectedValue=True, items=[
         'No context',
         'Sliding window',
         'Left-right neighborhood',
         'Containing segmentation'], orientation='horizontal', label='Mode:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Context specification mode.\n\nContexts define the rows of the resulting\ncrosstab.\n\n'No context': segments will be counted\nirrespective of their context (hence the output\ntable contains a single row).\n\n'Sliding window': contexts are defined as all the\nsuccessive, overlapping sequences of n segments\nin the 'Units' segmentation.\n\n'Left-right neighborhood': contexts are defined as\ndistinct combinations of segments occurring\nimmediately to the right and/or left of segments\nin the 'Units' segmentation.\n\n'Containing segmentation': contexts are defined\nas the distinct segments occurring in a given\nsegmentation (which may or may not be the same\nas the 'Units' segmentation).")
        self.slidingWindowBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.slidingWindowBox, height=3)
        self.windowSizeSpin = OWGUI.spin(widget=self.slidingWindowBox, master=self, value='windowSize', min=1, max=1, step=1, orientation='horizontal', label='Window size:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The length of segment sequences defining contexts.')
        self.leftRightNeighborhoodBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.leftRightNeighborhoodBox, height=3)
        self.leftContextSizeSpin = OWGUI.spin(widget=self.leftRightNeighborhoodBox, master=self, value='leftContextSize', min=0, max=1, step=1, orientation='horizontal', label='Left context size:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The length of segment sequences defining the\nleft side of contexts.')
        OWGUI.separator(widget=self.leftRightNeighborhoodBox, height=3)
        self.rightContextSizeSpin = OWGUI.spin(widget=self.leftRightNeighborhoodBox, master=self, value='rightContextSize', min=0, max=1, step=1, orientation='horizontal', label='Right context size:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The length of segment sequences defining the\nright side of contexts.')
        OWGUI.separator(widget=self.leftRightNeighborhoodBox, height=3)
        self.unitPosMarkerLineEdit = OWGUI.lineEdit(widget=self.leftRightNeighborhoodBox, master=self, value='unitPosMarker', orientation='horizontal', label='Unit position marker:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='A (possibly empty) string that will be used to\nindicate the separation between left and right\ncontext sides.')
        OWGUI.separator(widget=self.leftRightNeighborhoodBox, height=3)
        OWGUI.checkBox(widget=self.leftRightNeighborhoodBox, master=self, value='mergeStrings', label='Treat distinct strings as contiguous', callback=self.sendButton.settingsChanged, tooltip='Check this box if you want to treat separate strings\nas if they were actually contiguous, so that the end of\neach string is adjacent to the beginning of the next string.')
        self.containingSegmentationBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextSegmentationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='_contexts', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="The segmentation whose segment types define\nthe contexts in which segments of the 'Units'\nsegmentation will be counted.")
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextAnnotationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='contextAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether context types are defined by\nthe content of segments in the above specified\nsegmentation (value 'none') or by their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        OWGUI.checkBox(widget=self.containingSegmentationBox, master=self, value='mergeContexts', label='Merge contexts', callback=self.sendButton.settingsChanged, tooltip='Check this box if you want to treat all segments\nof the above specified segmentation as forming\na single context (hence the resulting crosstab\ncontains a single row).')
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
        if self.mode == 'Containing segmentation':
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
        """Check input, compute frequency tables, then send them"""
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
                table = Processor.count_in_window(units, window_size=self.windowSize, progress_callback=progressBar.advance)
                progressBar.finish()
            elif self.mode == 'Left-right neighborhood':
                num_iterations = len(units['segmentation']) - (self.leftContextSize + self.sequenceLength + self.rightContextSize - 1)
                progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
                table = Processor.count_in_chain(units, contexts={'left_size': self.leftContextSize, 
                   'right_size': self.rightContextSize, 
                   'unit_pos_marker': self.unitPosMarker, 
                   'merge_strings': self.mergeStrings}, progress_callback=progressBar.advance)
                progressBar.finish()
            else:
                if self.mode == 'Containing segmentation':
                    contexts = {'segmentation': self.segmentations[self._contexts][1], 'annotation_key': self.contextAnnotationKey or None, 
                       'merge': self.mergeContexts}
                    if contexts['annotation_key'] == '(none)':
                        contexts['annotation_key'] = None
                    num_iterations = len(contexts['segmentation'])
                else:
                    contexts = None
                    num_iterations = len(units['segmentation']) - (self.sequenceLength - 1)
                progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
                table = Processor.count_in_context(units, contexts, progress_callback=progressBar.advance)
                progressBar.finish()
            total = sum([ i for i in table.values.values() ])
            if total == 0:
                self.infoBox.setText('Resulting table is empty.', 'warning')
                self.send('Textable pivot crosstab', None)
                self.send('Orange table', None)
            else:
                if len(table.row_ids) == 1:
                    sortedTransposedTable = table.to_transposed().to_sorted(key_col_id=table.row_ids[0], reverse_rows=True)
                    self.send('Textable pivot crosstab', sortedTransposedTable)
                    self.send('Orange table', sortedTransposedTable.to_orange_table())
                else:
                    self.send('Textable pivot crosstab', table)
                    self.send('Orange table', table.to_orange_table())
                message = 'Table with %i occurrence@p sent to output.' % total
                message = pluralize(message, total)
                self.infoBox.setText(message)
            self.sendButton.resetSettingsChangedFlag()
            return

    def updateGUI(self):
        """Update GUI state"""
        self.unitSegmentationCombo.clear()
        self.unitAnnotationCombo.clear()
        self.unitAnnotationCombo.addItem('(none)')
        if self.mode == 'No context':
            self.containingSegmentationBox.setVisible(False)
            self.leftRightNeighborhoodBox.setVisible(False)
            self.slidingWindowBox.setVisible(False)
        if len(self.segmentations) == 0:
            self.units = None
            self.unitAnnotationKey = ''
            self.unitsBox.setDisabled(True)
            self.mode = 'No context'
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
            if self.mode == 'Sliding window':
                self.containingSegmentationBox.setVisible(False)
                self.leftRightNeighborhoodBox.setVisible(False)
                self.slidingWindowBox.setVisible(True)
                self.windowSizeSpin.control.setRange(self.sequenceLength, len(self.segmentations[self.units][1]))
                self.windowSize = self.windowSize or 1
            elif self.mode == 'Left-right neighborhood':
                self.containingSegmentationBox.setVisible(False)
                self.slidingWindowBox.setVisible(False)
                self.leftRightNeighborhoodBox.setVisible(True)
                self.leftContextSizeSpin.control.setRange(0, len(self.segmentations[self.units][1]) - self.sequenceLength - self.rightContextSize)
                self.leftContextSize = self.leftContextSize or 0
                self.rightContextSizeSpin.control.setRange(0, len(self.segmentations[self.units][1]) - self.sequenceLength - self.leftContextSize)
                self.rightContextSize = self.rightContextSize or 0
            elif self.mode == 'Containing segmentation':
                self.slidingWindowBox.setVisible(False)
                self.leftRightNeighborhoodBox.setVisible(False)
                self.containingSegmentationBox.setVisible(True)
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
    import LTTL.Segmenter as Segmenter
    from LTTL.Input import Input
    appl = QApplication(sys.argv)
    ow = OWTextableCount()
    seg1 = Input('hello world', label='text1')
    seg2 = Input('cruel world', label='text2')
    seg3 = Segmenter.concatenate([seg1, seg2], label='corpus')
    seg4 = Segmenter.tokenize(seg3, [
     (
      '\\w+(?u)', 'tokenize', {'type': 'mot'})], label='words')
    ow.inputData(seg3, 1)
    ow.inputData(seg4, 2)
    ow.show()
    appl.exec_()
    ow.saveSettings()