# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableVariety.py
# Compiled at: 2016-08-11 10:06:35
"""
Class OWTextableVariety
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
from LTTL.Table import Table
from LTTL.Segmentation import Segmentation
import LTTL.Processor as Processor
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableVariety(OWWidget):
    """Orange widget for mesuring variety of text units"""
    contextHandlers = {'': SegmentationListContextHandler('', [
          ContextInputListField('segmentations'),
          ContextInputIndex('units'),
          ContextInputIndex('_contexts'),
          'mode',
          'unitAnnotationKey',
          'categoryAnnotationKey',
          'contextAnnotationKey',
          'sequenceLength',
          'windowSize',
          'subsampleSize',
          'uuid'])}
    settingsList = [
     'autoSend',
     'sequenceLength',
     'measurePerCategory',
     'mode',
     'mergeContexts',
     'windowSize',
     'unitPosMarker',
     'unitWeighting',
     'categoryWeighting',
     'applyResampling',
     'numSubsamples',
     'subsampleSize']

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Variety widget"""
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
        self.mode = 'No context'
        self.mergeContexts = False
        self.windowSize = 1
        self.unitWeighting = False
        self.measurePerCategory = False
        self.categoryWeighting = False
        self.applyResampling = False
        self.numSubsamples = 100
        self.subsampleSize = 50
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentations = list()
        self.units = None
        self.unitAnnotationKey = None
        self.categoryAnnotationKey = None
        self._contexts = None
        self.contextAnnotationKey = None
        self.settingsRestored = False
        self.infoBox = InfoBox(widget=self.controlArea, stringClickSend=", please click 'Send' when ready.")
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', buttonLabel='Send', checkboxLabel='Send automatically', sendIfPreCallback=self.updateGUI)
        self.unitsBox = OWGUI.widgetBox(widget=self.controlArea, box='Units', orientation='vertical', addSpace=True)
        self.unitSegmentationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='units', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose variety will be measured.')
        self.unitSegmentationCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.unitAnnotationCombo = OWGUI.comboBox(widget=self.unitsBox, master=self, value='unitAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether the variety of the above\nspecified segmentation must be measured on the\nsegments' content (value 'none') or on their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.sequenceLengthSpin = OWGUI.spin(widget=self.unitsBox, master=self, value='sequenceLength', min=1, max=1, step=1, orientation='horizontal', label='Sequence length:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Indicate whether to measure the variety of\nsingle segments or rather of sequences of 2,\n3,... segments (n-grams).\n\nNote that this parameter cannot be set to a\nvalue larger than 1 if variety is to be\nmeasured per category.')
        OWGUI.separator(widget=self.unitsBox, height=3)
        OWGUI.checkBox(widget=self.unitsBox, master=self, value='unitWeighting', label='Weigh by frequency', callback=self.sendButton.settingsChanged, tooltip='Check this box in order to apply unit frequency\nweighting (i.e. use perplexity instead of variety).')
        OWGUI.separator(widget=self.unitsBox, height=3)
        self.categoriesBox = OWGUI.widgetBox(widget=self.controlArea, box='Categories', orientation='vertical', addSpace=True)
        self.measurePerCategoryCheckbox = OWGUI.checkBox(widget=self.categoriesBox, master=self, value='measurePerCategory', label='Measure variety per category', callback=self.sendButton.settingsChanged, tooltip='Check this box in order to measure the average\nvariety per category.')
        OWGUI.separator(widget=self.categoriesBox, height=3)
        iBox = OWGUI.indentedBox(widget=self.categoriesBox)
        self.categoryAnnotationCombo = OWGUI.comboBox(widget=iBox, master=self, value='categoryAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=160, callback=self.sendButton.settingsChanged, tooltip="Indicate whether categories are defined by the\nsegments' content (value 'none') or by their\nannotation values for a specific annotation key.")
        OWGUI.separator(widget=iBox, height=3)
        OWGUI.checkBox(widget=iBox, master=self, value='categoryWeighting', label='Weigh by frequency', callback=self.sendButton.settingsChanged, tooltip='Check this box in order to apply category\nfrequency weighting (i.e. compute a weighted\nrather than unweighted average).')
        self.measurePerCategoryCheckbox.disables.append(iBox)
        if self.measurePerCategory:
            iBox.setDisabled(False)
        else:
            iBox.setDisabled(True)
        OWGUI.separator(widget=self.categoriesBox, height=3)
        self.contextsBox = OWGUI.widgetBox(widget=self.controlArea, box='Contexts', orientation='vertical', addSpace=True)
        self.modeCombo = OWGUI.comboBox(widget=self.contextsBox, master=self, value='mode', sendSelectedValue=True, items=[
         'No context',
         'Sliding window',
         'Containing segmentation'], orientation='horizontal', label='Mode:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Context specification mode.\n\nContexts define the rows of the resulting\ntable.\n\n'No context': variety will be measured\nirrespective of the context (hence the output\ntable contains a single row).\n\n'Sliding window': contexts are defined as all the\nsuccessive, overlapping sequences of n segments\nin the 'Units' segmentation.\n\n'Containing segmentation': contexts are defined\nas the distinct segments occurring in a given\nsegmentation.")
        self.slidingWindowBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.slidingWindowBox, height=3)
        self.windowSizeSpin = OWGUI.spin(widget=self.slidingWindowBox, master=self, value='windowSize', min=1, max=1, step=1, orientation='horizontal', label='Window size:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The length of segment sequences defining contexts.')
        self.containingSegmentationBox = OWGUI.widgetBox(widget=self.contextsBox, orientation='vertical')
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextSegmentationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='_contexts', orientation='horizontal', label='Segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="The segmentation whose segment types define\nthe contexts in which the variety of segments\nin the 'Units' segmentation will be measured.")
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        self.contextAnnotationCombo = OWGUI.comboBox(widget=self.containingSegmentationBox, master=self, value='contextAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether context types are defined by\nthe content of segments in the above specified\nsegmentation (value 'none') or by their annotation\nvalues for a specific annotation key.")
        OWGUI.separator(widget=self.containingSegmentationBox, height=3)
        OWGUI.checkBox(widget=self.containingSegmentationBox, master=self, value='mergeContexts', label='Merge contexts', callback=self.sendButton.settingsChanged, tooltip='Check this box if you want to treat all segments\nof the above specified segmentation as forming\na single context (hence the resulting table\ncontains a single row).')
        OWGUI.separator(widget=self.contextsBox, height=3)
        self.resamplingBox = OWGUI.widgetBox(widget=self.controlArea, box='Resampling', orientation='vertical', addSpace=True)
        applyResamplingCheckBox = OWGUI.checkBox(widget=self.resamplingBox, master=self, value='applyResampling', label='Apply Resampling', callback=self.sendButton.settingsChanged, tooltip='Check this box if you want to compute the average\nvariety per subsample.')
        OWGUI.separator(widget=self.resamplingBox, height=3)
        iBox2 = OWGUI.indentedBox(widget=self.resamplingBox)
        self.subsampleSizeSpin = OWGUI.spin(widget=iBox2, master=self, value='subsampleSize', min=1, max=1, step=1, orientation='horizontal', label='Subsample size:', labelWidth=160, callback=self.sendButton.settingsChanged, tooltip='The number of segments per subsample.')
        OWGUI.separator(widget=iBox2, height=3)
        self.numSubsampleSpin = OWGUI.spin(widget=iBox2, master=self, value='numSubsamples', min=1, max=100000, step=1, orientation='horizontal', label='Number of subsamples:', labelWidth=160, callback=self.sendButton.settingsChanged, tooltip='The number of subsamples (per context).')
        applyResamplingCheckBox.disables.append(iBox2)
        if self.applyResampling:
            iBox2.setDisabled(False)
        else:
            iBox2.setDisabled(True)
        OWGUI.separator(widget=self.resamplingBox, height=3)
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
        """Check input, compute variety, then send table"""
        if len(self.segmentations) == 0:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Textable table', None)
            self.send('Orange table', None)
            return
        else:
            units = {'segmentation': self.segmentations[self.units][1], 
               'annotation_key': self.unitAnnotationKey or None, 
               'seq_length': self.sequenceLength, 
               'weighting': self.unitWeighting}
            if units['annotation_key'] == '(none)':
                units['annotation_key'] = None
            categories = {'annotation_key': self.categoryAnnotationKey or None, 
               'weighting': self.categoryWeighting}
            if categories['annotation_key'] == '(none)':
                categories['annotation_key'] = None
            if self.mode == 'Sliding window':
                num_iterations = len(units['segmentation']) - (self.windowSize - 1)
                if self.applyResampling:
                    num_iterations += num_iterations * self.numSubsamples
                else:
                    num_iterations *= 2
                progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
                table = Processor.variety_in_window(units, categories, measure_per_category=self.measurePerCategory, window_size=self.windowSize, apply_resampling=self.applyResampling, subsample_size=self.subsampleSize, num_subsamples=self.numSubsamples, progress_callback=progressBar.advance)
                progressBar.finish()
            else:
                if self.mode == 'Containing segmentation':
                    contexts = {'segmentation': self.segmentations[self._contexts][1], 'annotation_key': self.contextAnnotationKey or None, 
                       'merge': self.mergeContexts}
                    if contexts['annotation_key'] == '(none)':
                        contexts['annotation_key'] = None
                    num_contexts = len(contexts['segmentation'])
                    num_iterations = num_contexts
                else:
                    contexts = None
                    num_iterations = len(units['segmentation']) - (self.sequenceLength - 1)
                    num_contexts = 1
                if self.applyResampling:
                    num_iterations += num_contexts * self.numSubsamples
                else:
                    num_iterations += num_contexts
                progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
                table = Processor.variety_in_context(units, categories, contexts, measure_per_category=self.measurePerCategory, apply_resampling=self.applyResampling, subsample_size=self.subsampleSize, num_subsamples=self.numSubsamples, progress_callback=progressBar.advance)
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
        self.categoryAnnotationCombo.clear()
        self.categoryAnnotationCombo.addItem('(none)')
        if self.mode == 'No context':
            self.containingSegmentationBox.setVisible(False)
            self.slidingWindowBox.setVisible(False)
        if len(self.segmentations) == 0:
            self.units = None
            self.unitAnnotationKey = ''
            self.unitsBox.setDisabled(True)
            self.categoryAnnotationKey = ''
            self.categoriesBox.setDisabled(True)
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
                self.categoryAnnotationCombo.addItem(k)

            if self.unitAnnotationKey not in unitAnnotationKeys:
                self.unitAnnotationKey = '(none)'
            self.unitAnnotationKey = self.unitAnnotationKey
            if self.categoryAnnotationKey not in unitAnnotationKeys:
                self.categoryAnnotationKey = '(none)'
            self.categoryAnnotationKey = self.categoryAnnotationKey
            self.unitsBox.setDisabled(False)
            self.sequenceLengthSpin.control.setRange(1, len(self.segmentations[self.units][1]))
            self.sequenceLength = self.sequenceLength or 1
            if self.sequenceLength > 1:
                self.categoriesBox.setDisabled(True)
            else:
                self.categoriesBox.setDisabled(False)
            if self.measurePerCategory:
                self.sequenceLengthSpin.setDisabled(True)
            else:
                self.sequenceLengthSpin.setDisabled(False)
            self.contextsBox.setDisabled(False)
            self.subsampleSizeSpin.control.setRange(1, len(self.segmentations[self.units][1]))
            self.subsampleSize = self.subsampleSize or 1
            if self.mode == 'Sliding window':
                self.containingSegmentationBox.setVisible(False)
                self.slidingWindowBox.setVisible(True)
                self.windowSizeSpin.control.setRange(self.sequenceLength, len(self.segmentations[self.units][1]))
                self.windowSize = self.windowSize
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
    ow = OWTextableVariety()
    seg1 = Input('aabccc', 'text1')
    seg2 = Input('abci', 'text2')
    seg3 = Segmenter.concatenate([
     seg1, seg2], import_labels_as='string', label='corpus')
    seg4 = Segmenter.tokenize(seg3, regexes=[
     (
      re.compile('\\w+'), 'tokenize')])
    seg5 = Segmenter.tokenize(seg4, regexes=[
     (
      re.compile('[ai]'), 'tokenize')], label='V')
    seg6 = Segmenter.tokenize(seg4, regexes=[
     (
      re.compile('[bc]'), 'tokenize')], label='C')
    seg7 = Segmenter.concatenate([
     seg5, seg6], import_labels_as='category', label='letters', sort=True, merge_duplicates=True)
    ow.inputData(seg4, 1)
    ow.inputData(seg7, 2)
    ow.show()
    appl.exec_()
    ow.saveSettings()