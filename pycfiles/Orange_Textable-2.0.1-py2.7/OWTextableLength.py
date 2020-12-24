# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableLength.py
# Compiled at: 2016-08-11 10:06:40
"""
Class OWTextableLength
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
__version__ = '0.14.3'
from LTTL.Table import Table
from LTTL.Segmentation import Segmentation
import LTTL.Processor as Processor
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableLength(OWWidget):
    """Orange widget for length computation"""
    contextHandlers = {'': SegmentationListContextHandler('', [
          ContextInputListField('segmentations'),
          ContextInputIndex('units'),
          ContextInputIndex('averagingSegmentation'),
          ContextInputIndex('_contexts'),
          'mode',
          'unitAnnotationKey',
          'contextAnnotationKey',
          'sequenceLength'])}
    settingsList = [
     'autoSend',
     'computeStdev',
     'mergeContexts',
     'computeAverage',
     'sequenceLength']

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Length widget"""
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
        self.computeAverage = False
        self.computeStdev = False
        self.autoSend = False
        self.mode = 'No context'
        self.mergeContexts = False
        self.windowSize = 1
        self.loadSettings()
        self.segmentations = list()
        self.units = None
        self.averagingSegmentation = None
        self._contexts = None
        self.contextAnnotationKey = None
        self.settingsRestored = False
        self.infoBox = InfoBox(widget=self.controlArea, stringClickSend=", please click 'Send' when ready.")
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', buttonLabel='Send', checkboxLabel='Send automatically', sendIfPreCallback=self.updateGUI)
        self.unitsBox = OWGUI.widgetBox(widget=self.controlArea, box='Units', orientation='vertical', addSpace=True)
        self.unitSegmentationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='units', orientation='horizontal', label='Segmentation:', labelWidth=190, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segments constitute the\nunits of length.')
        self.unitSegmentationCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.averagingBox = OWGUI.widgetBox(widget=self.controlArea, box='Averaging', orientation='vertical', addSpace=True)
        averagingBoxLine1 = OWGUI.widgetBox(widget=self.averagingBox, box=False, orientation='horizontal', addSpace=True)
        OWGUI.checkBox(widget=averagingBoxLine1, master=self, value='computeAverage', label='Average over segmentation:', labelWidth=190, callback=self.sendButton.settingsChanged, tooltip='Check this box in order to measure the average\nlength of segments.\n\nLeaving this box unchecked implies that no\naveraging will take place.')
        self.averagingSegmentationCombo = OWGUI.comboBox(widget=averagingBoxLine1, master=self, value='averagingSegmentation', orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segment length will be\nmeasured and averaged (if the box to the left\nis checked).')
        self.computeStdevCheckBox = OWGUI.checkBox(widget=self.averagingBox, master=self, value='computeStdev', label='Compute standard deviation', callback=self.sendButton.settingsChanged, tooltip='Check this box to compute not only length average\nbut also standard deviation (if the above box\nis checked).\n\nNote that computing standard deviation can be a\nlengthy operation for large segmentations.')
        OWGUI.separator(widget=self.averagingBox, height=2)
        self.contextsBox = OWGUI.widgetBox(widget=self.controlArea, box='Contexts', orientation='vertical', addSpace=True)
        self.modeCombo = OWGUI.comboBox(widget=self.contextsBox, master=self, value='mode', sendSelectedValue=True, items=[
         'No context',
         'Sliding window',
         'Containing segmentation'], orientation='horizontal', label='Mode:', labelWidth=190, callback=self.sendButton.settingsChanged, tooltip="Context specification mode.\n\nContexts define the rows of the resulting table.\n\n'No context': simply return the length of the\n'Units' segmentation, or the average length of\nsegments in the 'Averaging' segmentation (if any),\nso that the output table contains a single row.\n\n'Sliding window': contexts are defined as all the\nsuccessive, overlapping sequences of n segments\nin the 'Averaging' segmentation; this mode is\navailable only if the 'Averaging' box is checked.\n\n'Containing segmentation': contexts are defined\nas the distinct segments occurring in a given\nsegmentation (which may or may not be the same\nas the 'Units' and/or 'Averaging' segmentation).")
        self.slidingWindowBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.slidingWindowBox, height=3)
        self.windowSizeSpin = OWGUI.spin(widget=self.slidingWindowBox, master=self, value='windowSize', min=1, max=1, step=1, orientation='horizontal', label='Window size:', labelWidth=190, callback=self.sendButton.settingsChanged, tooltip='The length of segment sequences defining contexts.')
        self.containingSegmentationBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextSegmentationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='_contexts', orientation='horizontal', label='Segmentation:', labelWidth=190, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose segment types define\nthe contexts in which length will be measured.')
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextAnnotationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='contextAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=190, callback=self.sendButton.settingsChanged, tooltip="Indicate whether context types are defined by\nthe content of segments in the above specified\nsegmentation (value 'none') or by their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        OWGUI.checkBox(widget=self.containingSegmentationBox, master=self, value='mergeContexts', label='Merge contexts', callback=self.sendButton.settingsChanged, tooltip='Check this box if you want to treat all segments\nof the above specified segmentation as forming\na single context (hence the resulting table\ncontains a single row).')
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

    def sendData(self):
        """Check input, compute (average) length table, then send it"""
        if len(self.segmentations) == 0:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Textable table', None)
            self.send('Orange table', None)
            return
        else:
            units = self.segmentations[self.units][1]
            if self.computeAverage:
                averaging = {'segmentation': self.segmentations[self.averagingSegmentation][1]}
                if self.computeStdev:
                    averaging['std_deviation'] = True
                else:
                    averaging['std_deviation'] = False
            else:
                averaging = None
            if self.mode == 'Sliding window':
                progressBar = OWGUI.ProgressBar(self, iterations=len(units) - (self.windowSize - 1))
                table = Processor.length_in_window(units, averaging=averaging, window_size=self.windowSize, progress_callback=progressBar.advance)
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
                    num_iterations = 1
                progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
                table = Processor.length_in_context(units, averaging, contexts, progress_callback=progressBar.advance)
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
        if self.computeAverage and self.averagingSegmentation != self.units:
            if index == self.averagingSegmentation:
                self.computeAverage = False
                self.averagingSegmentation = None
            elif index < self.averagingSegmentation:
                self.averagingSegmentation -= 1
                if self.averagingSegmentation < 0:
                    self.computeAverage = False
                    self.averagingSegmentation = None
        return

    def updateGUI(self):
        """Update GUI state"""
        self.unitSegmentationCombo.clear()
        self.averagingSegmentationCombo.clear()
        self.averagingSegmentationCombo.clear()
        if self.mode == 'No context':
            self.containingSegmentationBox.setVisible(False)
            self.slidingWindowBox.setVisible(False)
        if len(self.segmentations) == 0:
            self.units = None
            self.unitsBox.setDisabled(True)
            self.averagingBox.setDisabled(True)
            self.mode = 'No context'
            self.contextsBox.setDisabled(True)
            self.adjustSize()
            return
        else:
            if len(self.segmentations) == 1:
                self.units = 0
                self.averagingSegmentation = 0
            for segmentation in self.segmentations:
                self.unitSegmentationCombo.addItem(segmentation[1].label)
                self.averagingSegmentationCombo.addItem(segmentation[1].label)

            self.units = self.units
            self.averagingSegmentation = self.averagingSegmentation
            self.unitsBox.setDisabled(False)
            self.averagingBox.setDisabled(False)
            self.contextsBox.setDisabled(False)
            if self.computeAverage:
                if self.modeCombo.itemText(1) != 'Sliding window':
                    self.modeCombo.insertItem(1, 'Sliding window')
                self.averagingSegmentationCombo.setDisabled(False)
                self.computeStdevCheckBox.setDisabled(False)
            else:
                self.averagingSegmentationCombo.setDisabled(True)
                self.computeStdevCheckBox.setDisabled(True)
                self.computeStdev = False
                if self.mode == 'Sliding window':
                    self.mode = 'No context'
                if self.modeCombo.itemText(1) == 'Sliding window':
                    self.modeCombo.removeItem(1)
            if self.mode == 'Sliding window':
                self.containingSegmentationBox.setVisible(False)
                self.slidingWindowBox.setVisible(True)
                self.windowSizeSpin.control.setRange(1, len(self.segmentations[self.units][1]))
                self.windowSize = self.windowSize or 1
            elif self.mode == 'Containing segmentation':
                self.slidingWindowBox.setVisible(False)
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
    ow = OWTextableLength()
    seg1 = Input('hello world', label='text1')
    seg2 = Input('wonderful world', label='text2')
    seg3 = Segmenter.concatenate([seg1, seg2], label='corpus')
    seg4 = Segmenter.tokenize(seg3, [
     (
      '\\w+(?u)', 'tokenize')], label='words')
    seg5 = Segmenter.tokenize(seg3, [('\\w', 'tokenize')], label='letters')
    ow.inputData(seg3, 1)
    ow.inputData(seg4, 2)
    ow.inputData(seg5, 3)
    ow.show()
    appl.exec_()
    ow.saveSettings()