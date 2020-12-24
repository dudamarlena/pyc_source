# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable_prototypes\widgets\OWTextableTheatreClassique.py
# Compiled at: 2016-09-20 17:06:39
"""
Class OWTextableTheatreClassique
Copyright 2016 University of Lausanne
-----------------------------------------------------------------------------
This file is part of the Orange-Textable-Prototypes package v0.1.

Orange-Textable-Prototypes v0.1 is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as published 
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orange-Textable-Prototypes v0.1 is distributed in the hope that it will be 
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orange-Textable-Prototypes v0.1. If not, see 
<http://www.gnu.org/licenses/>.
"""
__version__ = '0.2.1'
__author__ = 'Aris Xanthos'
__maintainer__ = 'Aris Xanthos'
__email__ = 'aris.xanthos@unil.ch'
import Orange
from OWWidget import *
import OWGUI
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
import LTTL.Segmenter as Segmenter, LTTL.Processor as Processor
from _textable.widgets.TextableUtils import *
import urllib2, re, inspect, os, pickle

class OWTextableTheatreClassique(OWWidget):
    """Orange widget for importing XML-TEI data from the Theatre-classique
    website (http://www.theatre-classique.fr)
    """
    settingsList = [
     'autoSend',
     'label',
     'uuid',
     'selectedTitles',
     'filterCriterion',
     'filterValue',
     'importedURLs',
     'displayAdvancedSettings']

    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = []
        self.outputs = [
         (
          'Text data', Segmentation)]
        self.autoSend = True
        self.label = 'xml_tei_data'
        self.filterCriterion = 'author'
        self.filterValue = '(all)'
        self.titleLabels = list()
        self.selectedTitles = list()
        self.importedURLs = list()
        self.displayAdvancedSettings = False
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.segmentation = None
        self.createdInputs = list()
        self.titleSeg = None
        self.filteredTitleSeg = None
        self.filterValues = dict()
        self.base_url = 'http://www.theatre-classique.fr/pages/programmes/PageEdition.php'
        self.document_base_url = 'http://www.theatre-classique.fr/pages/'
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.updateGUI)
        self.advancedSettings = AdvancedSettings(widget=self.controlArea, master=self, callback=self.updateFilterValueList)
        self.advancedSettings.draw()
        filterBox = OWGUI.widgetBox(widget=self.controlArea, box='Filter', orientation='vertical')
        filterCriterionCombo = OWGUI.comboBox(widget=filterBox, master=self, value='filterCriterion', items=[
         'author', 'year', 'genre'], sendSelectedValue=True, orientation='horizontal', label='Criterion:', labelWidth=120, callback=self.updateFilterValueList, tooltip='Please select a criterion for searching the title list\n')
        filterCriterionCombo.setMinimumWidth(120)
        OWGUI.separator(widget=filterBox, height=3)
        self.filterValueCombo = OWGUI.comboBox(widget=filterBox, master=self, value='filterValue', sendSelectedValue=True, orientation='horizontal', label='Value:', labelWidth=120, callback=self.updateTitleList, tooltip='Please select a value for the chosen criterion.')
        OWGUI.separator(widget=filterBox, height=3)
        self.advancedSettings.advancedWidgets.append(filterBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        titleBox = OWGUI.widgetBox(widget=self.controlArea, box='Titles', orientation='vertical')
        self.titleListbox = OWGUI.listBox(widget=titleBox, master=self, value='selectedTitles', labels='titleLabels', callback=self.sendButton.settingsChanged, tooltip='The list of titles whose content will be imported')
        self.titleListbox.setMinimumHeight(150)
        self.titleListbox.setSelectionMode(3)
        OWGUI.separator(widget=titleBox, height=3)
        OWGUI.button(widget=titleBox, master=self, label='Refresh', callback=self.refreshTitleSeg, tooltip='Connect to Theatre-classique website and refresh list.')
        OWGUI.separator(widget=titleBox, height=3)
        OWGUI.separator(widget=self.controlArea, height=3)
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.getTitleSeg()
        self.sendButton.sendIf()
        self.setMinimumWidth(350)
        self.adjustSizeWithTimer()
        return

    def sendData(self):
        """Compute result of widget processing and send to output"""
        if self.titleLabels == list():
            return
        else:
            if len(self.selectedTitles) == 0:
                self.infoBox.setText('Please select one or more titles.', 'warning')
                self.send('Text data', None, self)
                return
            self.clearCreatedInputs()
            progressBar = OWGUI.ProgressBar(self, iterations=len(self.selectedTitles))
            xml_contents = list()
            annotations = list()
            try:
                for title in self.selectedTitles:
                    response = urllib2.urlopen(self.document_base_url + self.filteredTitleSeg[title].annotations['url'])
                    xml_contents.append(unicode(response.read(), 'utf8'))
                    annotations.append(self.filteredTitleSeg[title].annotations.copy())
                    progressBar.advance()

            except:
                self.infoBox.setText("Couldn't download data from theatre-classique website.", 'error')
                self.send('Text data', None, self)
                return

            for xml_content_idx in xrange(len(xml_contents)):
                newInput = Input(xml_contents[xml_content_idx], self.captionTitle)
                self.createdInputs.append(newInput)

            if len(self.createdInputs) == 1:
                self.segmentation = self.createdInputs[0]
            else:
                self.segmentation = Segmenter.concatenate(self.createdInputs, self.captionTitle, import_labels_as=None)
            for idx, segment in enumerate(self.segmentation):
                segment.annotations.update(annotations[idx])
                self.segmentation[idx] = segment

            self.importedURLs = [
             self.filteredTitleSeg[self.selectedTitles[0]].annotations['url']]
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
            progressBar.finish()
            self.send('Text data', self.segmentation, self)
            self.sendButton.resetSettingsChangedFlag()
            return

    def getTitleSeg(self):
        """Get title segmentation, either saved locally or online"""
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        try:
            file = open(os.path.join(path, 'cached_title_list'), 'rb')
            self.titleSeg = pickle.load(file)
            file.close()
        except IOError:
            self.titleSeg = self.getTitleListFromTheatreClassique()

        if self.titleSeg is not None:
            self.filterValues['author'] = Processor.count_in_context(units={'segmentation': self.titleSeg, 
               'annotation_key': 'author'}).col_ids
            self.filterValues['author'].sort()
            self.filterValues['year'] = Processor.count_in_context(units={'segmentation': self.titleSeg, 
               'annotation_key': 'year'}).col_ids
            self.filterValues['year'].sort(key=lambda v: int(v))
            self.filterValues['genre'] = Processor.count_in_context(units={'segmentation': self.titleSeg, 
               'annotation_key': 'genre'}).col_ids
            self.filterValues['genre'].sort()
        self.titleSeg.buffer.sort(key=lambda s: s.annotations['title'])
        self.updateFilterValueList()
        return

    def refreshTitleSeg(self):
        """Refresh title segmentation from website"""
        self.titleSeg = self.getTitleListFromTheatreClassique()
        self.updateFilterValueList()

    def getTitleListFromTheatreClassique(self):
        """Fetch titles from the Theatre-classique website"""
        self.infoBox.customMessage('Fetching data from Theatre-classique website, please wait')
        try:
            response = urllib2.urlopen(self.base_url)
            base_html = unicode(response.read(), 'iso-8859-1')
            self.infoBox.customMessage('Done fetching data from Theatre-classique website.')
        except:
            self.infoBox.noDataSent(warning="Couldn't access theatre-classique website.")
            self.titleLabels = list()
            self.send('Text data', None, self)
            return

        base_html_seg = Input(base_html)
        recoded_seg = Segmenter.recode(base_html_seg, remove_accents=True)
        table_seg = Segmenter.import_xml(segmentation=recoded_seg, element='table', conditions={'id': re.compile('^table_AA$')})
        line_seg = Segmenter.import_xml(segmentation=table_seg, element='tr')
        field_regex = re.compile("^\\s*<td>\\s*<a.+?>(.+?)</a>\\s*</td>\\s*<td>(.+?)</td>\\s*<td.+?>\\s*<a.+?>\\s*(\\d+?)\\s*</a>\\s*</td>\\s*<td.+?>\\s*(.+?)\\s*</td>\\s*<td.+?>\\s*<a\\s+.+?t=\\.{2}/(.+?)'>\\s*HTML")
        titleSeg = Segmenter.tokenize(segmentation=line_seg, regexes=[
         (
          field_regex, 'tokenize', {'author': '&1'}),
         (
          field_regex, 'tokenize', {'title': '&2'}),
         (
          field_regex, 'tokenize', {'year': '&3'}),
         (
          field_regex, 'tokenize', {'genre': '&4'}),
         (
          field_regex, 'tokenize', {'url': '&5'})], import_annotations=False, merge_duplicates=True)
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        try:
            file = open(os.path.join(path, 'cached_title_list'), 'wb')
            pickle.dump(titleSeg, file, -1)
            file.close()
        except IOError:
            pass

        self.error(0)
        self.warning(0)
        return titleSeg

    def updateFilterValueList(self):
        """Update the list of filter values"""
        if self.titleSeg is not None and self.displayAdvancedSettings:
            self.filterValueCombo.clear()
            self.filterValueCombo.addItem('(all)')
            for filterValue in self.filterValues[self.filterCriterion]:
                self.filterValueCombo.addItem(filterValue)

        if self.filterValue not in [ unicode(self.filterValueCombo.itemText(i)) for i in xrange(self.filterValueCombo.count())
                                   ]:
            self.filterValue = '(all)'
        else:
            self.filterValue = self.filterValue
        self.updateTitleList()
        return

    def updateTitleList(self):
        """Update the list of titles"""
        if self.titleSeg is None:
            return
        else:
            if self.displayAdvancedSettings and self.filterValue != '(all)':
                self.filteredTitleSeg, _ = Segmenter.select(segmentation=self.titleSeg, regex=re.compile('^%s$' % self.filterValue), annotation_key=self.filterCriterion)
            else:
                self.filteredTitleSeg = self.titleSeg
            self.titleLabels = sorted([ s.annotations['title'] for s in self.filteredTitleSeg ])
            titleLabels = self.titleLabels[:]
            for idx, titleLabel in enumerate(titleLabels):
                specs = list()
                if self.displayAdvancedSettings == False or self.filterCriterion != 'author' or self.filterValue == '(all)':
                    specs.append(self.filteredTitleSeg[idx].annotations['author'])
                if self.displayAdvancedSettings == False or self.filterCriterion != 'year' or self.filterValue == '(all)':
                    specs.append(self.filteredTitleSeg[idx].annotations['year'])
                if self.displayAdvancedSettings == False or self.filterCriterion != 'genre' or self.filterValue == '(all)':
                    specs.append(self.filteredTitleSeg[idx].annotations['genre'])
                titleLabels[idx] = titleLabel + ' (%s)' % ('; ').join(specs)

            self.titleLabels = titleLabels
            if not set(self.importedURLs).issubset(set(u.annotations['url'] for u in self.filteredTitleSeg)):
                self.selectedTitles = list()
            else:
                self.selectedTitles = self.selectedTitles
            self.sendButton.settingsChanged()
            return

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
        if len(self.titleLabels) > 0:
            self.selectedTitles = self.selectedTitles

    def clearCreatedInputs(self):
        """Delete all Input objects that have been created."""
        for i in self.createdInputs:
            Segmentation.set_data(i[0].str_index, None)

        del self.createdInputs[:]
        return

    def onDeleteWidget(self):
        """Free memory when widget is deleted (overriden method)"""
        self.clearCreatedInputs()

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
        """Read settings, taking into account version number (overriden)"""
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings['settingsDataVersion'] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        """Write settings, taking into account version number (overriden)"""
        if settings.get('settingsDataVersion', None) == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings['settingsDataVersion']
            OWWidget.setSettings(self, settings)
        return


if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTextableTheatreClassique()
    myWidget.show()
    myApplication.exec_()