# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableSelect.py
# Compiled at: 2016-07-01 03:18:09
"""
Class OWTextableSelect
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
from __future__ import division
__version__ = '0.14.2'
import re, math, LTTL.Segmenter as Segmenter
from LTTL.Segmentation import Segmentation
from LTTL.Utils import iround
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableSelect(OWWidget):
    """Orange widget for segment in-/exclusion based on intrinsic properties"""
    contextHandlers = {'': SegmentationContextHandler('', [
          'regexAnnotationKey',
          'thresholdAnnotationKeysampleSize',
          'minCount',
          'maxCount'])}
    settingsList = [
     'regex',
     'method',
     'regexMode',
     'ignoreCase',
     'unicodeDependent',
     'multiline',
     'dotAll',
     'sampleSizeMode',
     'sampleSize',
     'samplingRate',
     'thresholdMode',
     'applyMinThreshold',
     'applyMaxThreshold',
     'minCount',
     'maxCount',
     'minProportion',
     'maxProportion',
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
          'Segmentation', Segmentation, self.inputData, Single)]
        self.outputs = [
         (
          'Selected data', Segmentation, Default),
         (
          'Discarded data', Segmentation)]
        self.method = 'Regex'
        self.copyAnnotations = True
        self.autoSend = False
        self.autoNumber = False
        self.autoNumberKey = 'num'
        self.regex = ''
        self.regexMode = 'Include'
        self.ignoreCase = False
        self.unicodeDependent = True
        self.multiline = False
        self.dotAll = False
        self.sampleSizeMode = 'Count'
        self.sampleSize = 1
        self.samplingRate = 1
        self.thresholdMode = 'Count'
        self.applyMinThreshold = True
        self.applyMaxThreshold = True
        self.minCount = 1
        self.maxCount = 1
        self.minProportion = 1
        self.maxProportion = 100
        self.displayAdvancedSettings = False
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentation = None
        self.regexAnnotationKey = None
        self.thresholdAnnotationKey = None
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.updateGUI)
        self.advancedSettings = AdvancedSettings(widget=self.controlArea, master=self, callback=self.sendButton.settingsChanged)
        self.advancedSettings.draw()
        self.selectBox = OWGUI.widgetBox(widget=self.controlArea, box='Select', orientation='vertical')
        self.methodCombo = OWGUI.comboBox(widget=self.selectBox, master=self, value='method', sendSelectedValue=True, items=[
         'Regex', 'Sample', 'Threshold'], orientation='horizontal', label='Method:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Selection mode.\n\n'Regex': segments are selected based on content\nor annotation pattern matching.\n\n'Sample': segments are selected based on random\nor systematic sampling.\n\n'Threshold': segments are selected based on the\nfrequency of the corresponding type (content or\nannotation value).")
        self.methodCombo.setMinimumWidth(120)
        OWGUI.separator(widget=self.selectBox, height=3)
        self.regexBox = OWGUI.widgetBox(widget=self.selectBox, orientation='vertical')
        self.regexModeCombo = OWGUI.comboBox(widget=self.regexBox, master=self, value='regexMode', sendSelectedValue=True, items=[
         'Include', 'Exclude'], orientation='horizontal', label='Mode:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Specify whether input segments matching the regex\npattern should be included in or excluded from\nthe output segmentation.')
        OWGUI.separator(widget=self.regexBox, height=3)
        self.regexAnnotationCombo = OWGUI.comboBox(widget=self.regexBox, master=self, value='regexAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether the regex pattern specified\nbelow should be applied to annotation values\ncorresponding to a specific annotation key or\ndirectly to the content of input segments (value\n'none').")
        OWGUI.separator(widget=self.regexBox, height=3)
        OWGUI.lineEdit(widget=self.regexBox, master=self, value='regex', orientation='horizontal', label='Regex:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The regex pattern that must be matched by input\nsegments content or annotation values in order\nfor the segment to be included in or excluded\nfrom the output segmentation.')
        OWGUI.separator(widget=self.regexBox, height=3)
        regexBoxLine4 = OWGUI.widgetBox(widget=self.regexBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=regexBoxLine4, master=self, value='ignoreCase', label='Ignore case (i)', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Regex pattern is case-insensitive.')
        OWGUI.checkBox(widget=regexBoxLine4, master=self, value='unicodeDependent', label='Unicode dependent (u)', callback=self.sendButton.settingsChanged, tooltip='Built-in character classes are Unicode-aware.')
        regexBoxLine5 = OWGUI.widgetBox(widget=self.regexBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=regexBoxLine5, master=self, value='multiline', label='Multiline (m)', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Anchors '^' and '$' match the beginning and\nend of each line (rather than just the beginning\nand end of each input segment).")
        OWGUI.checkBox(widget=regexBoxLine5, master=self, value='dotAll', label='Dot matches all (s)', callback=self.sendButton.settingsChanged, tooltip="Meta-character '.' matches any character (rather\nthan any character but newline).")
        OWGUI.separator(widget=self.regexBox, height=3)
        self.sampleBox = OWGUI.widgetBox(widget=self.selectBox, orientation='vertical')
        self.sampleSizeModeCombo = OWGUI.comboBox(widget=self.sampleBox, master=self, value='sampleSizeMode', sendSelectedValue=True, items=[
         'Count', 'Proportion'], orientation='horizontal', label='Sample size expressed as:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Specify whether sample size will be expressed as\na number of tokens (value 'Count') or as a given\nproportion of the input segments ('Proportion').")
        OWGUI.separator(widget=self.sampleBox, height=3)
        self.sampleSizeSpin = OWGUI.spin(widget=self.sampleBox, master=self, value='sampleSize', min=1, max=1, orientation='horizontal', label='Sample size:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The number of segments that will be sampled.')
        self.samplingRateSpin = OWGUI.spin(widget=self.sampleBox, master=self, value='samplingRate', min=1, max=100, orientation='horizontal', label='Sampling rate (%):', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The proportion of segments that will be sampled.')
        OWGUI.separator(widget=self.sampleBox, height=3)
        self.thresholdBox = OWGUI.widgetBox(widget=self.selectBox, orientation='vertical')
        self.thresholdAnnotationCombo = OWGUI.comboBox(widget=self.thresholdBox, master=self, value='thresholdAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether the frequency thresholds\nspecified below should be applied to annotation\nvalues corresponding to a specific annotation\nkey or directly to the content of input segments\n(value 'none').")
        OWGUI.separator(widget=self.thresholdBox, height=3)
        self.thresholdModeCombo = OWGUI.comboBox(widget=self.thresholdBox, master=self, value='thresholdMode', sendSelectedValue=True, items=[
         'Count', 'Proportion'], orientation='horizontal', label='Threshold expressed as:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Specify whether frequency thresholds will be\nexpressed as numbers of tokens (value 'Count')\nor as relative frequencies (value 'Proportion').")
        OWGUI.separator(widget=self.thresholdBox, height=3)
        self.minCountLine = OWGUI.widgetBox(widget=self.thresholdBox, box=False, orientation='horizontal')
        self.minCountSpin = OWGUI.checkWithSpin(widget=self.minCountLine, master=self, value='minCount', label='Min. count:', labelWidth=180, controlWidth=None, checked='applyMinThreshold', min=1, max=100, spinCallback=self.sendButton.settingsChanged, checkCallback=self.sendButton.settingsChanged, tooltip='Minimum count for a type to be selected.')
        self.minProportionLine = OWGUI.widgetBox(widget=self.thresholdBox, box=False, orientation='horizontal')
        self.minProportionSpin = OWGUI.checkWithSpin(widget=self.minProportionLine, master=self, value='minProportion', label='Min. proportion (%):', labelWidth=180, controlWidth=None, checked='applyMinThreshold', min=1, max=100, spinCallback=self.sendButton.settingsChanged, checkCallback=self.sendButton.settingsChanged, tooltip='Minimum relative frequency for a type to be selected.')
        OWGUI.separator(widget=self.thresholdBox, height=3)
        self.maxCountLine = OWGUI.widgetBox(widget=self.thresholdBox, box=False, orientation='horizontal')
        self.maxCountSpin = OWGUI.checkWithSpin(widget=self.maxCountLine, master=self, value='maxCount', label='Max. count:', labelWidth=180, controlWidth=None, checked='applyMaxThreshold', min=1, max=100, spinCallback=self.sendButton.settingsChanged, checkCallback=self.sendButton.settingsChanged, tooltip='Maximum count for a type to be selected.')
        self.maxProportionLine = OWGUI.widgetBox(widget=self.thresholdBox, box=False, orientation='horizontal')
        self.maxProportionSpin = OWGUI.checkWithSpin(widget=self.maxProportionLine, master=self, value='maxProportion', label='Max. proportion (%):', labelWidth=180, controlWidth=None, checked='applyMaxThreshold', min=1, max=100, spinCallback=self.sendButton.settingsChanged, checkCallback=self.sendButton.settingsChanged, tooltip='Maximum count for a type to be selected.')
        OWGUI.separator(widget=self.thresholdBox, height=3)
        self.advancedSettings.advancedWidgets.append(self.selectBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        optionsBox = OWGUI.widgetBox(widget=self.controlArea, box='Options', orientation='vertical')
        optionsBoxLine2 = OWGUI.widgetBox(widget=optionsBox, box=False, orientation='horizontal')
        OWGUI.checkBox(widget=optionsBoxLine2, master=self, value='autoNumber', label='Auto-number with key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Annotate output segments with increasing numeric\nindices.')
        self.autoNumberKeyLineEdit = OWGUI.lineEdit(widget=optionsBoxLine2, master=self, value='autoNumberKey', orientation='horizontal', callback=self.sendButton.settingsChanged, tooltip='Annotation key for output segment auto-numbering.')
        OWGUI.separator(widget=optionsBox, height=3)
        OWGUI.checkBox(widget=optionsBox, master=self, value='copyAnnotations', label='Copy annotations', callback=self.sendButton.settingsChanged, tooltip='Copy all annotations from input to output segments.')
        OWGUI.separator(widget=optionsBox, height=2)
        self.advancedSettings.advancedWidgets.append(optionsBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        self.basicSelectBox = OWGUI.widgetBox(widget=self.controlArea, box='Select', orientation='vertical')
        self.basicRegexModeCombo = OWGUI.comboBox(widget=self.basicSelectBox, master=self, value='regexMode', sendSelectedValue=True, items=[
         'Include', 'Exclude'], orientation='horizontal', label='Mode:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Specify whether input segments matching the regex\npattern should be included in or excluded from\nthe output segmentation.')
        OWGUI.separator(widget=self.basicSelectBox, height=3)
        self.basicRegexAnnotationCombo = OWGUI.comboBox(widget=self.basicSelectBox, master=self, value='regexAnnotationKey', sendSelectedValue=True, emptyString='(none)', orientation='horizontal', label='Annotation key:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip="Indicate whether the regex pattern specified\nbelow should be applied to annotation values\ncorresponding to a specific annotation key or\ndirectly to the content of input segments (value\n'none').")
        OWGUI.separator(widget=self.basicSelectBox, height=3)
        OWGUI.lineEdit(widget=self.basicSelectBox, master=self, value='regex', orientation='horizontal', label='Regex:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='The regex pattern that must be matched by input\nsegments content or annotation values in order\nfor the segment to be included in or excluded\nfrom the output segmentation.')
        OWGUI.separator(widget=self.basicSelectBox, height=3)
        self.advancedSettings.basicWidgets.append(self.basicSelectBox)
        self.advancedSettings.basicWidgetsAppendSeparator()
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def sendData(self):
        """(Have LTTL.Segmenter) perform the actual selection"""
        if not self.segmentation:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Selected data', None, self)
            self.send('Discarded data', None, self)
            return
        if self.displayAdvancedSettings:
            if self.method == 'Regex':
                if not self.regex:
                    self.infoBox.setText('Please enter a regex.', 'warning')
                    self.send('Selected data', None, self)
                    self.send('Discarded data', None, self)
                    return
                regex_string = self.regex
                if self.ignoreCase or self.unicodeDependent or self.multiline or self.dotAll:
                    flags = ''
                    if self.ignoreCase:
                        flags += 'i'
                    if self.unicodeDependent:
                        flags += 'u'
                    if self.multiline:
                        flags += 'm'
                    if self.dotAll:
                        flags += 's'
                    regex_string += '(?%s)' % flags
                try:
                    regex = re.compile(regex_string)
                except re.error as re_error:
                    message = 'Please enter a valid regex (error: %s).' % re_error.message
                    self.infoBox.setText(message, 'error')
                    self.send('Selected data', None, self)
                    self.send('Discarded data', None, self)
                    return

                num_iterations = len(self.segmentation)
            elif self.method == 'Sample':
                if self.sampleSizeMode == 'Proportion':
                    sampleSize = iround(len(self.segmentation) * (self.samplingRate / 100))
                else:
                    sampleSize = self.sampleSize
                if sampleSize <= 0:
                    self.infoBox.setText(message='Please enter a larger sample size', state='error')
                    self.send('Selected data', None, self)
                    self.send('Discarded data', None, self)
                    return
                num_iterations = len(self.segmentation)
            elif self.method == 'Threshold':
                if self.thresholdMode == 'Proportion':
                    minCount = iround(math.ceil(len(self.segmentation) * (self.minProportion / 100)))
                    maxCount = iround(math.floor(len(self.segmentation) * (self.maxProportion / 100)))
                else:
                    minCount = self.minCount
                    maxCount = self.maxCount
                if not self.applyMinThreshold:
                    minCount = 1
                if not self.applyMaxThreshold:
                    maxCount = len(self.segmentation)
                num_iterations = len(self.segmentation)
            if self.autoNumber:
                if self.autoNumberKey:
                    autoNumberKey = self.autoNumberKey
                else:
                    self.infoBox.setText('Please enter an annotation key for auto-numbering.', 'warning')
                    self.send('Selected data', None, self)
                    self.send('Discarded data', None, self)
                    return
            else:
                autoNumberKey = None
            progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
            if self.method == 'Regex':
                regexAnnotationKeyParam = self.regexAnnotationKey
                if regexAnnotationKeyParam == '(none)':
                    regexAnnotationKeyParam = None
                selected_data, discarded_data = Segmenter.select(segmentation=self.segmentation, regex=regex, mode=self.regexMode.lower(), annotation_key=regexAnnotationKeyParam or None, label=self.captionTitle, copy_annotations=self.copyAnnotations, auto_number_as=autoNumberKey, progress_callback=progressBar.advance)
            elif self.method == 'Sample':
                selected_data, discarded_data = Segmenter.sample(segmentation=self.segmentation, sample_size=sampleSize, mode='random', label=self.captionTitle, copy_annotations=self.copyAnnotations, auto_number_as=autoNumberKey, progress_callback=progressBar.advance)
            elif self.method == 'Threshold':
                if (minCount == 1 or not self.applyMinThreshold) and (maxCount == len(self.segmentation) or not self.applyMaxThreshold):
                    selected_data = Segmenter.bypass(segmentation=self.segmentation, label=self.captionTitle)
                    discarded_data = None
                else:
                    thresholdAnnotationKeyParam = self.thresholdAnnotationKey
                    if thresholdAnnotationKeyParam == '(none)':
                        thresholdAnnotationKeyParam = None
                    selected_data, discarded_data = Segmenter.threshold(segmentation=self.segmentation, annotation_key=thresholdAnnotationKeyParam or None, min_count=minCount, max_count=maxCount, label=self.captionTitle, copy_annotations=self.copyAnnotations, auto_number_as=autoNumberKey, progress_callback=progressBar.advance)
        else:
            if not self.regex:
                self.infoBox.setText('Please enter a regex.', 'warning')
                self.send('Selected data', None, self)
                self.send('Discarded data', None, self)
                return
            num_iterations = len(self.segmentation)
            progressBar = OWGUI.ProgressBar(self, iterations=num_iterations)
            regexAnnotationKeyParam = self.regexAnnotationKey
            if regexAnnotationKeyParam == '(none)':
                regexAnnotationKeyParam = None
            try:
                selected_data, discarded_data = Segmenter.select(segmentation=self.segmentation, regex=re.compile(self.regex + '(?u)'), mode=self.regexMode.lower(), annotation_key=regexAnnotationKeyParam or None, label=self.captionTitle, copy_annotations=True, auto_number_as=None, progress_callback=progressBar.advance)
            except re.error as re_error:
                message = 'Please enter a valid regex (error: %s).' % re_error.message
                self.infoBox.setText(message, 'error')
                self.send('Selected data', None, self)
                self.send('Discarded data', None, self)
                progressBar.finish()
                return

        progressBar.finish()
        message = '%i segment@p sent to output.' % len(selected_data)
        message = pluralize(message, len(selected_data))
        self.infoBox.setText(message)
        self.send('Selected data', selected_data, self)
        self.send('Discarded data', discarded_data, self)
        self.sendButton.resetSettingsChangedFlag()
        return

    def inputData(self, segmentation):
        """Process incoming segmentation"""
        self.closeContext()
        self.segmentation = segmentation
        self.infoBox.inputChanged()
        self.updateGUI()
        if segmentation is not None:
            self.openContext('', segmentation)
        self.sendButton.sendIf()
        return

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings and self.autoNumber:
            self.autoNumberKeyLineEdit.setDisabled(False)
        else:
            self.autoNumberKeyLineEdit.setDisabled(True)
        self.selectBox.setDisabled(not self.segmentation)
        self.basicSelectBox.setDisabled(not self.segmentation)
        if self.displayAdvancedSettings:
            if self.method == 'Regex':
                self.sampleBox.setVisible(False)
                self.thresholdBox.setVisible(False)
                self.regexAnnotationCombo.clear()
                self.regexAnnotationCombo.addItem('(none)')
                if self.segmentation is not None:
                    for k in self.segmentation.get_annotation_keys():
                        self.regexAnnotationCombo.addItem(k)

                    self.regexAnnotationKey = self.regexAnnotationKey
                self.regexBox.setVisible(True)
            elif self.method == 'Sample':
                self.regexBox.setVisible(False)
                self.thresholdBox.setVisible(False)
                if self.sampleSizeMode == 'Count':
                    self.samplingRateSpin.setVisible(False)
                    if self.segmentation is not None and len(self.segmentation):
                        self.sampleSizeSpin.control.setRange(1, len(self.segmentation))
                        if self.sampleSize > len(self.segmentation):
                            self.sampleSize = len(self.segmentation)
                    else:
                        self.sampleSizeSpin.control.setRange(1, 1)
                    self.sampleSize = self.sampleSize or 1
                    self.sampleSizeSpin.setVisible(True)
                elif self.sampleSizeMode == 'Proportion':
                    self.sampleSizeSpin.setVisible(False)
                    self.samplingRate = self.samplingRate or 1
                    self.samplingRateSpin.setVisible(True)
                self.sampleBox.setVisible(True)
            elif self.method == 'Threshold':
                self.regexBox.setVisible(False)
                self.sampleBox.setVisible(False)
                self.thresholdAnnotationCombo.clear()
                self.thresholdAnnotationCombo.addItem('(none)')
                if self.segmentation is not None:
                    for k in self.segmentation.get_annotation_keys():
                        self.thresholdAnnotationCombo.addItem(k)

                    self.thresholdAnnotationKey = self.thresholdAnnotationKey
                if self.thresholdMode == 'Count':
                    self.minProportionLine.setVisible(False)
                    self.maxProportionLine.setVisible(False)
                    if self.segmentation is not None and len(self.segmentation):
                        self.maxCount = self.maxCount or len(self.segmentation)
                        if self.applyMaxThreshold:
                            maxValue = self.maxCount
                        else:
                            maxValue = len(self.segmentation)
                        self.minCountSpin[1].setRange(1, maxValue)
                        self.minCount = self.minCount or 1
                        if self.applyMinThreshold:
                            minValue = self.minCount
                        else:
                            minValue = 1
                        self.maxCountSpin[1].setRange(minValue, len(self.segmentation))
                    else:
                        self.minCountSpin[1].setRange(1, 1)
                        self.maxCountSpin[1].setRange(1, 1)
                    self.minCountLine.setVisible(True)
                    self.maxCountLine.setVisible(True)
                elif self.thresholdMode == 'Proportion':
                    self.minCountLine.setVisible(False)
                    self.maxCountLine.setVisible(False)
                    if self.segmentation is not None and len(self.segmentation):
                        if self.applyMaxThreshold:
                            maxValue = self.maxProportion
                        else:
                            maxValue = 100
                        self.minProportionSpin[1].setRange(1, maxValue)
                        self.minProportion = self.minProportion or 1
                        if self.applyMinThreshold:
                            minValue = self.minProportion
                        else:
                            minValue = 1
                        self.maxProportionSpin[1].setRange(minValue, 100)
                        self.maxProportion = self.maxProportion or 100
                    else:
                        self.minProportionSpin[1].setRange(1, 100)
                        self.maxProportionSpin[1].setRange(1, 100)
                    self.minProportionLine.setVisible(True)
                    self.maxProportionLine.setVisible(True)
                self.thresholdBox.setVisible(True)
            self.advancedSettings.setVisible(True)
        else:
            self.basicRegexAnnotationCombo.clear()
            self.basicRegexAnnotationCombo.addItem('(none)')
            if self.segmentation is not None:
                for k in self.segmentation.get_annotation_keys():
                    self.basicRegexAnnotationCombo.addItem(k)

                self.regexAnnotationKey = self.regexAnnotationKey
            self.advancedSettings.setVisible(False)
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
    ow = OWTextableSelect()
    ow.show()
    appl.exec_()
    ow.saveSettings()