# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableIntersect.py
# Compiled at: 2016-07-01 03:18:09
"""
Class OWTextableIntersect
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
__version__ = '0.15.0'
import LTTL.Segmenter as Segmenter
from LTTL.Segmentation import Segmentation
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableIntersect(OWWidget):
    """Orange widget for segment in-/exclusion based on other segmentation"""
    contextHandlers = {'': SegmentationListContextHandler('', [
          ContextInputListField('segmentations'),
          ContextInputIndex('source'),
          ContextInputIndex('filtering'),
          'sourceAnnotationKey',
          'filteringAnnotationKey'])}
    settingsList = [
     'mode',
     'copyAnnotations',
     'autoSend',
     'autoNumber',
     'autoNumberKey',
     'displayAdvancedSettings',
     'uuid']

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Segmentation', Segmentation, self.inputData, Multiple)]
        self.outputs = [
         (
          'Selected data', Segmentation, Default),
         (
          'Discarded data', Segmentation)]
        self.copyAnnotations = True
        self.autoSend = False
        self.mode = 'Include'
        self.autoNumber = False
        self.autoNumberKey = 'num'
        self.displayAdvancedSettings = False
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentations = list()
        self.source = None
        self.sourceAnnotationKey = None
        self.filtering = None
        self.filteringAnnotationKey = None
        self.settingsRestored = False
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.updateGUI)
        self.advancedSettings = AdvancedSettings(widget=self.controlArea, master=self, callback=self.sendButton.settingsChanged)
        self.advancedSettings.draw()
        self.intersectBox = OWGUI.widgetBox(widget=self.controlArea, box='Intersect', orientation='vertical')
        self.modeCombo = OWGUI.comboBox(widget=self.intersectBox, master=self, value='mode', sendSelectedValue=True, items=[
         'Include', 'Exclude'], orientation='horizontal', label='Mode:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Specify whether source segments whose type is\npresent in the filter segmentation should be\nincluded in or excluded from the output\nsegmentation.')
        self.modeCombo.setMinimumWidth(140)
        OWGUI.separator(widget=self.intersectBox, height=3)
        self.sourceCombo = OWGUI.comboBox(widget=self.intersectBox, master=self, value='source', orientation='horizontal', label='Source segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation from which a subset of segments\nwill be selected to build the output segmentation.')
        OWGUI.separator(widget=self.intersectBox, height=3)
        self.sourceAnnotationCombo = OWGUI.comboBox(widget=self.intersectBox, master=self, value='sourceAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Source annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether source segments will be selected\nbased on annotation values corresponding to a\nspecific annotation key or rather on their content\n(value 'none').")
        OWGUI.separator(widget=self.intersectBox, height=3)
        self.filteringCombo = OWGUI.comboBox(widget=self.intersectBox, master=self, value='filtering', orientation='horizontal', label='Filter segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose types will be used to\ninclude source segments in (or exclude them from)\nthe output segmentation.')
        OWGUI.separator(widget=self.intersectBox, height=3)
        self.filteringAnnotationCombo = OWGUI.comboBox(widget=self.intersectBox, master=self, value='filteringAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Filter annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether filter segment types are based\non annotation values corresponding to a specific\nannotation key or rather on segment content\n(value 'none').")
        OWGUI.separator(widget=self.intersectBox, height=3)
        self.advancedSettings.advancedWidgets.append(self.intersectBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        optionsBox = OWGUI.widgetBox(widget=self.controlArea, box='Options', orientation='vertical')
        optionsBoxLine2 = OWGUI.widgetBox(widget=optionsBox, box=False, orientation='horizontal', addSpace=True)
        OWGUI.checkBox(widget=optionsBoxLine2, master=self, value='autoNumber', label='Auto-number with key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Annotate output segments with increasing numeric\nindices.')
        self.autoNumberKeyLineEdit = OWGUI.lineEdit(widget=optionsBoxLine2, master=self, value='autoNumberKey', orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='Annotation key for output segment auto-numbering.')
        OWGUI.checkBox(widget=optionsBox, master=self, value='copyAnnotations', label='Copy annotations', callback=self.sendButton.settingsChanged, tooltip='Copy all annotations from input to output segments.')
        OWGUI.separator(widget=optionsBox, height=2)
        self.advancedSettings.advancedWidgets.append(optionsBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        self.basicIntersectBox = OWGUI.widgetBox(widget=self.controlArea, box='Intersect', orientation='vertical')
        self.basicModeCombo = OWGUI.comboBox(widget=self.basicIntersectBox, master=self, value='mode', sendSelectedValue=True, items=[
         'Include', 'Exclude'], orientation='horizontal', label='Mode:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Specify whether source segments whose type is\npresent in the filter segmentation should be\nincluded in or excluded from the output\nsegmentation.')
        self.basicModeCombo.setMinimumWidth(140)
        OWGUI.separator(widget=self.basicIntersectBox, height=3)
        self.basicSourceCombo = OWGUI.comboBox(widget=self.basicIntersectBox, master=self, value='source', orientation='horizontal', label='Source segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation from which a subset of segments\nwill be selected to build the output segmentation.')
        OWGUI.separator(widget=self.basicIntersectBox, height=3)
        self.basicFilteringCombo = OWGUI.comboBox(widget=self.basicIntersectBox, master=self, value='filtering', orientation='horizontal', label='Filter segmentation:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The segmentation whose types will be used to\ninclude source segments in (or exclude them from)\nthe output segmentation.')
        OWGUI.separator(widget=self.basicIntersectBox, height=3)
        self.advancedSettings.basicWidgets.append(self.basicIntersectBox)
        self.advancedSettings.basicWidgetsAppendSeparator()
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def sendData(self):
        """(Have LTTL.Segmenter) perform the actual filtering"""
        if len(self.segmentations) == 0:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Selected data', None, self)
            self.send('Discarded data', None, self)
            return
        else:
            source = self.segmentations[self.source][1]
            filtering = self.segmentations[self.filtering][1]
            if self.displayAdvancedSettings:
                source_annotation_key = self.sourceAnnotationKey or None
                if self.sourceAnnotationKey == '(none)':
                    source_annotation_key = None
                filtering_annotation_key = self.filteringAnnotationKey or None
                if filtering_annotation_key == '(none)':
                    filtering_annotation_key = None
            else:
                source_annotation_key = None
                filtering_annotation_key = None
            if self.displayAdvancedSettings and self.autoNumber:
                if self.autoNumberKey:
                    autoNumberKey = self.autoNumberKey
                    num_iterations = 2 * len(source['segmentation'])
                else:
                    self.infoBox.setText('Please enter an annotation key for auto-numbering.', 'warning')
                    self.send('Selected data', None, self)
                    self.send('Discarded data', None, self)
                    return
            else:
                autoNumberKey = None
                num_iterations = len(source)
            if self.displayAdvancedSettings:
                copyAnnotations = self.copyAnnotations
            else:
                copyAnnotations = True
            progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
            filtered_data, discarded_data = Segmenter.intersect(source=source, source_annotation_key=source_annotation_key, filtering=filtering, filtering_annotation_key=filtering_annotation_key, mode=self.mode.lower(), label=self.captionTitle, copy_annotations=self.copyAnnotations, auto_number_as=autoNumberKey, progress_callback=progressBar.advance)
            progressBar.finish()
            message = '%i segment@p sent to output.' % len(filtered_data)
            message = pluralize(message, len(filtered_data))
            self.infoBox.setText(message)
            self.send('Selected data', filtered_data, self)
            self.send('Discarded data', discarded_data, self)
            self.sendButton.resetSettingsChangedFlag()
            return

    def inputData(self, newItem, newId=None):
        """Process incoming data."""
        self.closeContext()
        updateMultipleInputs(self.segmentations, newItem, newId, self.onInputRemoval)
        self.infoBox.inputChanged()
        self.updateGUI()

    def onInputRemoval(self, index):
        """Handle removal of input with given index"""
        if index < self.source:
            self.source -= 1
        elif index == self.source and self.source == len(self.segmentations) - 1:
            self.source -= 1
            if self.source < 0:
                self.source = None
        if index < self.filtering:
            self.filtering -= 1
        elif index == self.filtering and self.filtering == len(self.segmentations) - 1:
            self.filtering -= 1
            if self.filtering < 0:
                self.filtering = None
        return

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            sourceCombo = self.sourceCombo
            filteringCombo = self.filteringCombo
            intersectBox = self.intersectBox
        else:
            sourceCombo = self.basicSourceCombo
            filteringCombo = self.basicFilteringCombo
            intersectBox = self.basicIntersectBox
        sourceCombo.clear()
        self.sourceAnnotationCombo.clear()
        self.sourceAnnotationCombo.addItem('(none)')
        self.advancedSettings.setVisible(self.displayAdvancedSettings)
        if len(self.segmentations) == 0:
            self.source = None
            self.sourceAnnotationKey = ''
            intersectBox.setDisabled(True)
            self.adjustSize()
            return
        else:
            if len(self.segmentations) == 1:
                self.source = 0
            for segmentation in self.segmentations:
                sourceCombo.addItem(segmentation[1].label)

            self.source = self.source
            sourceAnnotationKeys = self.segmentations[self.source][1].get_annotation_keys()
            for k in sourceAnnotationKeys:
                self.sourceAnnotationCombo.addItem(k)

            if self.sourceAnnotationKey not in sourceAnnotationKeys:
                self.sourceAnnotationKey = '(none)'
            self.sourceAnnotationKey = self.sourceAnnotationKey
            intersectBox.setDisabled(False)
            self.autoNumberKeyLineEdit.setDisabled(not self.autoNumber)
            filteringCombo.clear()
            for index in range(len(self.segmentations)):
                filteringCombo.addItem(self.segmentations[index][1].label)

            self.filtering = self.filtering or 0
            segmentation = self.segmentations[self.filtering]
            if self.displayAdvancedSettings:
                self.filteringAnnotationCombo.clear()
                self.filteringAnnotationCombo.addItem('(none)')
                filteringAnnotationKeys = segmentation[1].get_annotation_keys()
                for key in filteringAnnotationKeys:
                    self.filteringAnnotationCombo.addItem(key)

                if self.filteringAnnotationKey not in filteringAnnotationKeys:
                    self.filteringAnnotationKey = '(none)'
                self.filteringAnnotationKey = self.filteringAnnotationKey
            self.adjustSize()
            self.adjustSizeWithTimer()
            return

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def setCaption(self, title):
        if 'captionTitle' in dir(self) and title != 'Orange Widget':
            OWWidget.setCaption(self, title)
            self.sendButton.settingsChanged()
        else:
            OWWidget.setCaption(self, title)

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
    appl = QApplication(sys.argv)
    ow = OWTextableIntersect()
    seg1 = Input('hello world', 'text')
    seg2 = Segmenter.tokenize(seg1, [
     (
      re.compile('hello'), 'tokenize', {'tag': 'interj'}),
     (
      re.compile('world'), 'tokenize', {'tag': 'noun'})], label='words')
    seg3 = Segmenter.tokenize(seg2, [
     (
      re.compile('[aeiou]'), 'tokenize')], label='V')
    seg4 = Segmenter.tokenize(seg2, [
     (
      re.compile('[hlwrdc]'), 'tokenize')], label='C')
    seg5 = Segmenter.tokenize(seg2, [
     (
      re.compile(' '), 'tokenize')], label='S')
    seg6 = Segmenter.concatenate([
     seg3, seg4, seg5], import_labels_as='category', label='chars', sort=True, merge_duplicates=True)
    seg7 = Segmenter.tokenize(seg6, [
     (
      re.compile('l'), 'tokenize')], label='pivot')
    ow.inputData(seg2, 1)
    ow.inputData(seg6, 2)
    ow.inputData(seg7, 3)
    ow.show()
    appl.exec_()
    ow.saveSettings()