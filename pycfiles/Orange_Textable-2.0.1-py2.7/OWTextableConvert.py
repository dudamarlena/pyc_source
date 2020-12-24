# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\OWTextableConvert.py
# Compiled at: 2016-10-10 07:11:02
"""
Class OWTextableConvert
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
__version__ = '0.19.4'
import codecs
from LTTL.Table import *
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
from TextableUtils import *
from Orange.OrangeWidgets.OWWidget import *
import OWGUI

class OWTextableConvert(OWWidget):
    """Orange widget for converting a Textable table to an Orange table"""
    settingsList = [
     'conversionEncoding',
     'exportEncoding',
     'colDelimiter',
     'includeOrangeHeaders',
     'sortRows',
     'sortRowsReverse',
     'sortCols',
     'sortColsReverse',
     'normalize',
     'normalizeMode',
     'normalizeType',
     'convert',
     'conversionType',
     'associationBias',
     'transpose',
     'reformat',
     'unweighted',
     'autoSend',
     'lastLocation',
     'displayAdvancedSettings']
    encodings = getPredefinedEncodings()

    def __init__(self, parent=None, signalManager=None):
        """Initialize a Convert widget"""
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0, wantStateInfoWidget=0)
        self.inputs = [
         (
          'Textable table', Table, self.inputData, Single)]
        self.outputs = [
         (
          'Orange table', Orange.data.Table, Default),
         (
          'Textable table', Table),
         (
          'Segmentation', Segmentation)]
        self.sortRows = False
        self.sortRowsReverse = False
        self.sortCols = False
        self.sortColsReverse = False
        self.normalize = False
        self.normalizeMode = 'rows'
        self.normalizeType = 'l1'
        self.convert = False
        self.conversionType = 'association matrix'
        self.associationBias = 'none'
        self.transpose = False
        self.reformat = False
        self.unweighted = False
        self.autoSend = True
        self.conversionEncoding = 'iso-8859-15'
        self.exportEncoding = 'utf-8'
        self.colDelimiter = '\t'
        self.includeOrangeHeaders = False
        self.lastLocation = '.'
        self.displayAdvancedSettings = False
        self.loadSettings()
        self.sortRowsKeyId = None
        self.sortColsKeyId = None
        self.table = None
        self.segmentation = None
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(widget=self.controlArea, master=self, callback=self.sendData, infoBoxAttribute='infoBox', sendIfPreCallback=self.updateGUI)
        self.advancedSettings = AdvancedSettings(widget=self.controlArea, master=self, callback=self.sendButton.settingsChanged)
        self.advancedSettings.draw()
        self.transformBox = OWGUI.widgetBox(widget=self.controlArea, box='Transform', orientation='vertical')
        self.transformBoxLine1 = OWGUI.widgetBox(widget=self.transformBox, orientation='horizontal')
        OWGUI.checkBox(widget=self.transformBoxLine1, master=self, value='sortRows', label='Sort rows by column:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Sort table rows.')
        self.sortRowsKeyIdCombo = OWGUI.comboBox(widget=self.transformBoxLine1, master=self, value='sortRowsKeyId', items=list(), callback=self.sendButton.settingsChanged, tooltip='Column whose values will be used for sorting rows.')
        self.sortRowsKeyIdCombo.setMinimumWidth(150)
        OWGUI.separator(widget=self.transformBoxLine1, width=5)
        self.sortRowsReverseCheckBox = OWGUI.checkBox(widget=self.transformBoxLine1, master=self, value='sortRowsReverse', label='Reverse', callback=self.sendButton.settingsChanged, tooltip='Sort rows in reverse (i.e. decreasing) order.')
        OWGUI.separator(widget=self.transformBox, height=3)
        self.transformBoxLine2 = OWGUI.widgetBox(widget=self.transformBox, orientation='horizontal')
        OWGUI.checkBox(widget=self.transformBoxLine2, master=self, value='sortCols', label='Sort columns by row:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Sort table columns.')
        self.sortColsKeyIdCombo = OWGUI.comboBox(widget=self.transformBoxLine2, master=self, value='sortColsKeyId', items=list(), callback=self.sendButton.settingsChanged, tooltip='Row whose values will be used for sorting columns.')
        self.sortColsKeyIdCombo.setMinimumWidth(150)
        OWGUI.separator(widget=self.transformBoxLine2, width=5)
        self.sortColsReverseCheckBox = OWGUI.checkBox(widget=self.transformBoxLine2, master=self, value='sortColsReverse', label='Reverse', callback=self.sendButton.settingsChanged, tooltip='Sort columns in reverse (i.e. decreasing) order.')
        OWGUI.separator(widget=self.transformBox, height=3)
        self.transposeCheckBox = OWGUI.checkBox(widget=self.transformBox, master=self, value='transpose', label='Transpose', callback=self.sendButton.settingsChanged, tooltip='Transpose table (i.e. exchange rows and columns).')
        OWGUI.separator(widget=self.transformBox, height=3)
        self.transformBoxLine4 = OWGUI.widgetBox(widget=self.transformBox, orientation='horizontal')
        OWGUI.checkBox(widget=self.transformBoxLine4, master=self, value='normalize', label='Normalize:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Normalize table.')
        self.normalizeModeCombo = OWGUI.comboBox(widget=self.transformBoxLine4, master=self, value='normalizeMode', items=[
         'rows',
         'columns',
         'quotients',
         'TF-IDF',
         'presence/absence'], sendSelectedValue=True, callback=self.sendButton.settingsChanged, tooltip='Normalization mode:\n\nRow: L1 or L2 normalization by rows.\n\nColumn: L1 or L2 normalization by columns.\n\nQuotients: the count stored in each cell is\ndivided by the corresponding theoretical count\nunder independence: the result is greater than 1\nin case of attraction between line and column,\nlesser than 1 in case of repulsion, and 1 if\nthere is no specific interaction between them.\n\nTF-IDF: the count stored in each cell is multiplied\nby the natural log of the ratio of the number of\nrows (i.e. contexts) having nonzero count for this\ncolumn (i.e. unit) to the total number of rows.\n\nPresence/absence: counts greater than 0 are\nreplaced with 1.')
        self.normalizeModeCombo.setMinimumWidth(150)
        OWGUI.separator(widget=self.transformBoxLine4, width=5)
        self.normalizeTypeCombo = OWGUI.comboBox(widget=self.transformBoxLine4, master=self, orientation='horizontal', value='normalizeType', items=[
         'L1', 'L2'], sendSelectedValue=True, label='Norm:', labelWidth=40, callback=self.sendButton.settingsChanged, tooltip='Norm type.\n\nL1: divide each value by the sum of the enclosing\nnormalization unit (row/column)\n\nL2: divide each value by the sum of squares of the\nenclosing normalization unit, then take square root.')
        self.normalizeTypeCombo.setMinimumWidth(70)
        OWGUI.separator(widget=self.transformBox, height=3)
        self.transformBoxLine5 = OWGUI.widgetBox(widget=self.transformBox, orientation='horizontal')
        OWGUI.checkBox(widget=self.transformBoxLine5, master=self, value='convert', label='Convert to:', labelWidth=180, callback=self.sendButton.settingsChanged, tooltip='Apply crosstab conversions.')
        self.conversionTypeCombo = OWGUI.comboBox(widget=self.transformBoxLine5, master=self, value='conversionType', items=[
         'document frequency',
         'association matrix'], sendSelectedValue=True, callback=self.sendButton.settingsChanged, tooltip="Crosstab conversions.\n\n'document frequency': based on a pivot crosstab,\nreturn a new crosstab giving, for each column,\nthe number of distinct rows that have nonzero\nfrequency (hence the resulting crosstab contains\na single row).\n\n'association matrix': based on a pivot crosstab,\nreturn a symmetric table with a measure of\nassociativity between each pair of columns of the\noriginal table (see also the effect of the 'bias'\nparameter).")
        self.conversionTypeCombo.setMinimumWidth(150)
        OWGUI.separator(widget=self.transformBoxLine5, width=5)
        self.associationBiasCombo = OWGUI.comboBox(widget=self.transformBoxLine5, master=self, orientation='horizontal', value='associationBias', items=[
         'frequent', 'none', 'rare'], sendSelectedValue=True, label='Bias:', labelWidth=40, callback=self.sendButton.settingsChanged, tooltip="Association bias (alpha parameter in Deneulin,\nGautier, Le Fur, & Bavaud 2014).\n\n'frequent': emphasizes strong associations\nbetween frequent units (alpha=1).\n\n'none': balanced compromise between\nfrequent and rare units (alpha=0.5).\n\n'rare': emphasizes strong associations\nbetween rare units (alpha=0). Note that in this\nparticular case, values greater than 1 express an\nattraction and values lesser than 1 a repulsion.")
        self.associationBiasCombo.setMinimumWidth(70)
        OWGUI.separator(widget=self.transformBox, height=3)
        self.transformBoxLine6 = OWGUI.widgetBox(widget=self.transformBox, orientation='vertical')
        self.reformatCheckbox = OWGUI.checkBox(widget=self.transformBoxLine6, master=self, value='reformat', label='Reformat to sparse crosstab', callback=self.sendButton.settingsChanged, tooltip="Reformat a crosstab to sparse format, where each\nrow corresponds to a pair 'row-column' of the\noriginal crosstab.")
        OWGUI.separator(widget=self.transformBoxLine6, height=3)
        iBox = OWGUI.indentedBox(widget=self.transformBoxLine6)
        self.unweightedCheckbox = OWGUI.checkBox(widget=iBox, master=self, value='unweighted', label='Encode counts by repeating rows', callback=self.sendButton.settingsChanged, tooltip="This option (only available for crosstabs with\ninteger values) specifies that values will be\nencoded in the sparse matrix by the number of\ntimes each row (i.e. each pair row-column of the\noriginal crosstab) is repeated. Otherwise each\nrow-column pair will appear only once and the\ncorresponding value will be stored explicitely\nin a separate column with label '__weight__'.\n")
        OWGUI.separator(widget=self.transformBox, height=3)
        self.advancedSettings.advancedWidgets.append(self.transformBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        dummyBox = OWGUI.widgetBox(widget=self.controlArea, addSpace=False)
        self.advancedSettings.basicWidgets.append(dummyBox)
        encodingBox = OWGUI.widgetBox(widget=self.controlArea, box='Encoding', orientation='vertical', addSpace=True)
        encodingBoxLine1 = OWGUI.widgetBox(widget=encodingBox, orientation='horizontal')
        OWGUI.widgetLabel(widget=encodingBoxLine1, labelWidth=180, label='Orange table:')
        conversionEncodingCombo = OWGUI.comboBox(widget=encodingBoxLine1, master=self, value='conversionEncoding', items=type(self).encodings, sendSelectedValue=True, callback=self.sendButton.settingsChanged, orientation='horizontal', tooltip="Select the encoding of the Orange table that is\nsent on the widget's output connections.\n\nNote that utf-8 and other variants of Unicode are\nusually not well supported by standard Orange\nwidgets.")
        conversionEncodingCombo.setMinimumWidth(150)
        OWGUI.separator(widget=encodingBoxLine1, width=5)
        OWGUI.widgetLabel(widget=encodingBoxLine1, label='')
        OWGUI.separator(widget=encodingBox, height=3)
        encodingBoxLine2 = OWGUI.widgetBox(widget=encodingBox, orientation='horizontal')
        OWGUI.widgetLabel(widget=encodingBoxLine2, labelWidth=180, label='Output file:')
        conversionEncodingCombo = OWGUI.comboBox(widget=encodingBoxLine2, master=self, value='exportEncoding', items=type(self).encodings, sendSelectedValue=True, callback=self.sendButton.settingsChanged, orientation='horizontal', tooltip="Select the encoding of the table that can be\nsaved to a file by clicking the 'Export' button\nbelow.\n\nNote that the table that is copied to the\nclipboard by clicking the 'Copy to clipboard'\nbutton below is always encoded in utf-8.")
        conversionEncodingCombo.setMinimumWidth(150)
        OWGUI.separator(widget=encodingBoxLine2, width=5)
        OWGUI.widgetLabel(widget=encodingBoxLine2, label='')
        OWGUI.separator(widget=encodingBox, height=3)
        exportBox = OWGUI.widgetBox(widget=self.controlArea, box='Export', orientation='vertical', addSpace=False)
        exportBoxLine2 = OWGUI.widgetBox(widget=exportBox, orientation='horizontal')
        OWGUI.widgetLabel(widget=exportBoxLine2, labelWidth=180, label='Column delimiter:')
        colDelimiterCombo = OWGUI.comboBox(widget=exportBoxLine2, master=self, value='colDelimiter', callback=self.sendButton.settingsChanged, orientation='horizontal', items=[
         'tabulation (\\t)',
         'comma (,)',
         'semi-colon (;)'], sendSelectedValue=True, control2attributeDict={'tabulation (\\t)': '\t', 
           'comma (,)': ',', 
           'semi-colon (;)': ';'}, tooltip='Select the character used for delimiting columns.')
        colDelimiterCombo.setMinimumWidth(150)
        OWGUI.separator(widget=exportBoxLine2, width=5)
        dummyLabel = OWGUI.widgetLabel(widget=exportBoxLine2, label='')
        OWGUI.separator(widget=exportBox, height=2)
        OWGUI.checkBox(widget=exportBox, master=self, value='includeOrangeHeaders', label='Include Orange headers', tooltip='Include Orange table headers in output file.')
        OWGUI.separator(widget=exportBox, height=2)
        exportBoxLine3 = OWGUI.widgetBox(widget=exportBox, orientation='horizontal')
        self.exportButton = OWGUI.button(widget=exportBoxLine3, master=self, label='Export to file', callback=self.exportFile, tooltip='Open a dialog for selecting the output file to\nwhich the table will be saved.')
        self.copyButton = OWGUI.button(widget=exportBoxLine3, master=self, label='Copy to clipboard', callback=self.copyToClipboard, tooltip='Copy table to clipboard, in order to paste it in\nanother application (typically in a spreadsheet).\n\nNote that the only possible encoding is utf-8.')
        OWGUI.separator(widget=exportBox, height=2)
        self.advancedSettings.advancedWidgets.append(exportBox)
        basicExportBox = OWGUI.widgetBox(widget=self.controlArea, box='Export', orientation='vertical', addSpace=True)
        basicExportBoxLine1 = OWGUI.widgetBox(widget=basicExportBox, orientation='horizontal')
        self.basicExportButton = OWGUI.button(widget=basicExportBoxLine1, master=self, label='Export to file', callback=self.exportFile, tooltip='Open a dialog for selecting the output file to\nwhich the table will be saved.')
        self.basicCopyButton = OWGUI.button(widget=basicExportBoxLine1, master=self, label='Copy to clipboard', callback=self.copyToClipboard, tooltip='Copy table to clipboard, in order to paste it in\nanother application (typically in a spreadsheet).\n\nNote that the only possible encoding is utf-8.')
        OWGUI.separator(widget=basicExportBox, height=2)
        self.advancedSettings.basicWidgets.append(basicExportBox)
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()
        return

    def inputData(self, newInput):
        """Process incoming data."""
        self.table = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()

    def sendData(self):
        """Convert and send table"""
        if not self.table:
            self.infoBox.setText('Widget needs input.', 'warning')
            self.send('Orange table', None)
            self.send('Textable table', None)
            self.send('Segmentation', None, self)
            if self.segmentation is not None:
                self.segmentation.clear()
                self.segmentation = None
            return
        transformed_table = self.table
        if self.displayAdvancedSettings:
            numIterations = 0
            if self.transpose:
                num_cols = len(transformed_table.row_ids)
                num_rows = len(transformed_table.col_ids)
            else:
                num_rows = len(transformed_table.row_ids)
                num_cols = len(transformed_table.col_ids)
            if self.normalize:
                if self.normalizeMode == 'rows':
                    numIterations += num_rows
                elif self.normalizeMode == 'columns':
                    numIterations += num_cols
                elif self.normalizeMode == 'presence/absence':
                    numIterations += num_cols * num_rows
                elif self.normalizeMode == 'quotients':
                    numIterations += num_cols * (num_rows + 1)
                elif self.normalizeMode == 'TF-IDF':
                    numIterations += num_cols
            elif self.convert:
                numIterations += num_cols
            if self.reformat:
                numIterations += num_rows
            progressBar = OWGUI.ProgressBar(self, numIterations)
            if self.sortRows or self.sortCols:
                if self.sortRows:
                    if self.sortRowsKeyId == 0:
                        key_col_id = transformed_table.header_col_id
                    else:
                        key_col_id = transformed_table.col_ids[(self.sortRowsKeyId - 1)]
                else:
                    key_col_id = None
                if self.sortCols:
                    if self.sortColsKeyId == 0:
                        key_row_id = transformed_table.header_row_id
                    else:
                        key_row_id = transformed_table.row_ids[(self.sortColsKeyId - 1)]
                else:
                    key_row_id = None
                transformed_table = transformed_table.to_sorted(key_col_id, self.sortRowsReverse, key_row_id, self.sortColsReverse)
            if self.transpose:
                transformed_table = transformed_table.to_transposed()
            if self.normalize:
                transformed_table = transformed_table.to_normalized(self.normalizeMode, self.normalizeType.lower(), progressBar.advance)
            elif self.convert:
                if self.conversionType == 'document frequency':
                    transformed_table = transformed_table.to_document_frequency(progress_callback=progressBar.advance)
                elif self.conversionType == 'association matrix':
                    transformed_table = transformed_table.to_association_matrix(bias=self.associationBias, progress_callback=progressBar.advance)
            if self.reformat:
                if self.unweighted:
                    transformed_table = transformed_table.to_flat(progress_callback=progressBar.advance)
                else:
                    transformed_table = transformed_table.to_weighted_flat(progress_callback=progressBar.advance)
            progressBar.finish()
        self.transformed_table = transformed_table
        orangeTable = transformed_table.to_orange_table(encoding=self.conversionEncoding)
        self.send('Orange table', orangeTable)
        self.send('Textable table', transformed_table)
        if self.displayAdvancedSettings:
            colDelimiter = self.colDelimiter
            includeOrangeHeaders = self.includeOrangeHeaders
        else:
            colDelimiter = '\t'
            includeOrangeHeaders = False
        outputString = transformed_table.to_string(output_orange_headers=includeOrangeHeaders, col_delimiter=colDelimiter)
        if self.segmentation is None:
            self.segmentation = Input(label='table', text=outputString)
        else:
            self.segmentation.update(outputString, label='table')
        self.send('Segmentation', self.segmentation, self)
        message = 'Table with %i row@p' % len(transformed_table.row_ids)
        message = pluralize(message, len(transformed_table.row_ids))
        message += ' and %i column@p ' % (len(transformed_table.col_ids) + 1)
        message = pluralize(message, len(transformed_table.col_ids) + 1)
        message += 'sent to output.'
        self.infoBox.setText(message)
        self.sendButton.resetSettingsChangedFlag()
        return

    def exportFile(self):
        """Display a FileDialog and save table to file"""
        if getattr(self, self.sendButton.changedFlag):
            QMessageBox.warning(None, 'Textable', "Input data and/or settings have changed.\nPlease click 'Send' or check 'Send automatically' before proceeding.", QMessageBox.Ok)
            return
        else:
            filePath = unicode(QFileDialog.getSaveFileName(self, 'Export Table to File', self.lastLocation))
            if filePath:
                self.lastLocation = os.path.dirname(filePath)
                outputFile = codecs.open(filePath, encoding=self.exportEncoding, mode='w', errors='xmlcharrefreplace')
                outputFile.write(self.segmentation[0].get_content())
                outputFile.close()
                QMessageBox.information(None, 'Textable', 'Table successfully exported to file.', QMessageBox.Ok)
            return

    def copyToClipboard(self):
        """Copy output table to clipboard"""
        if getattr(self, self.sendButton.changedFlag):
            QMessageBox.warning(None, 'Textable', "Input data and/or settings have changed.\nPlease click 'Send' or check 'Send automatically' before proceeding.", QMessageBox.Ok)
            return
        else:
            QApplication.clipboard().setText(self.segmentation[0].get_content())
            QMessageBox.information(None, 'Textable', 'Table successfully copied to clipboard.', QMessageBox.Ok)
            return

    def updateGUI(self):
        """Update GUI state"""
        if not self.table:
            if self.displayAdvancedSettings:
                self.transformBox.setDisabled(True)
                self.exportButton.setDisabled(True)
                self.copyButton.setDisabled(True)
            else:
                self.basicExportButton.setDisabled(True)
                self.basicCopyButton.setDisabled(True)
        else:
            if self.displayAdvancedSettings:
                self.transformBox.setDisabled(False)
                self.exportButton.setDisabled(False)
                self.copyButton.setDisabled(False)
            else:
                self.basicExportButton.setDisabled(False)
                self.basicCopyButton.setDisabled(False)
            if self.displayAdvancedSettings:
                self.normalizeTypeCombo.setDisabled(True)
                self.associationBiasCombo.setDisabled(True)
                if self.sortRows:
                    self.sortRowsKeyIdCombo.clear()
                    self.sortRowsKeyIdCombo.addItem(unicode(self.table.header_col_id))
                    if isinstance(self.table.col_ids[0], (int, long)):
                        tableColIds = [ unicode(i) for i in self.table.col_ids ]
                    else:
                        tableColIds = self.table.col_ids
                    for col_id in tableColIds:
                        self.sortRowsKeyIdCombo.addItem(unicode(col_id))

                    self.sortRowsKeyId = self.sortRowsKeyId or 0
                    self.sortRowsKeyIdCombo.setDisabled(False)
                    self.sortRowsReverseCheckBox.setDisabled(False)
                else:
                    self.sortRowsKeyIdCombo.setDisabled(True)
                    self.sortRowsKeyIdCombo.clear()
                    self.sortRowsReverseCheckBox.setDisabled(True)
                if self.sortCols:
                    self.sortColsKeyIdCombo.clear()
                    self.sortColsKeyIdCombo.addItem(unicode(self.table.header_row_id))
                    if isinstance(self.table.row_ids[0], (int, long)):
                        tableRowIds = [ unicode(i) for i in self.table.row_ids ]
                    else:
                        tableRowIds = self.table.row_ids
                    for row_id in tableRowIds:
                        self.sortColsKeyIdCombo.addItem(unicode(row_id))

                    self.sortColsKeyId = self.sortColsKeyId or 0
                    self.sortColsKeyIdCombo.setDisabled(False)
                    self.sortColsReverseCheckBox.setDisabled(False)
                else:
                    self.sortColsKeyIdCombo.setDisabled(True)
                    self.sortColsKeyIdCombo.clear()
                    self.sortColsReverseCheckBox.setDisabled(True)
                if isinstance(self.table, Crosstab):
                    self.transposeCheckBox.setDisabled(False)
                    self.transformBoxLine4.setDisabled(False)
                    self.transformBoxLine5.setDisabled(False)
                    self.transformBoxLine6.setDisabled(False)
                    self.normalizeModeCombo.setDisabled(True)
                    self.normalizeTypeCombo.setDisabled(True)
                    self.conversionTypeCombo.setDisabled(True)
                    self.associationBiasCombo.setDisabled(True)
                    self.reformatCheckbox.setDisabled(False)
                    self.unweightedCheckbox.setDisabled(False)
                    if isinstance(self.table, IntPivotCrosstab):
                        if self.normalize:
                            self.normalizeModeCombo.setDisabled(False)
                            self.transformBoxLine5.setDisabled(True)
                            self.convert = False
                            self.unweightedCheckbox.setDisabled(True)
                            self.unweighted = False
                            if self.normalizeMode == 'rows' or self.normalizeMode == 'columns':
                                self.normalizeTypeCombo.setDisabled(False)
                        elif self.convert:
                            self.conversionTypeCombo.setDisabled(False)
                            self.transformBoxLine4.setDisabled(True)
                            self.normalize = False
                            self.unweightedCheckbox.setDisabled(True)
                            self.unweighted = False
                            if self.conversionType == 'association matrix':
                                self.associationBiasCombo.setDisabled(False)
                        if self.reformat:
                            if self.unweighted:
                                self.transformBoxLine4.setDisabled(True)
                                self.normalize = False
                                self.transformBoxLine5.setDisabled(True)
                                self.convert = False
                        else:
                            self.unweightedCheckbox.setDisabled(True)
                    else:
                        self.transformBoxLine4.setDisabled(True)
                        self.normalize = False
                        self.transformBoxLine5.setDisabled(True)
                        self.convert = False
                        self.unweightedCheckbox.setDisabled(True)
                    if isinstance(self.table, PivotCrosstab):
                        self.transposeCheckBox.setDisabled(False)
                else:
                    self.transposeCheckBox.setDisabled(True)
                    self.transpose = False
                    self.transformBoxLine4.setDisabled(True)
                    self.normalize = False
                    self.transformBoxLine5.setDisabled(True)
                    self.convert = False
                    self.transformBoxLine6.setDisabled(True)
                    self.reformat = False
        self.advancedSettings.setVisible(self.displayAdvancedSettings)
        self.adjustSizeWithTimer()

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def onDeleteWidget(self):
        if self.segmentation is not None:
            self.segmentation.clear()
        return

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
    ow = OWTextableConvert()
    ow.show()
    t = IntPivotCrosstab([
     'c', 'a', 'b'], [
     'B', 'C', 'A'], {('a', 'A'): 2, 
       ('a', 'B'): 3, 
       ('b', 'A'): 4, 
       ('b', 'C'): 2, 
       ('c', 'A'): 1, 
       ('c', 'B'): 4, 
       ('c', 'C'): 1}, header_row_id='__unit__', header_row_type='discrete', header_col_id='__context__', header_col_type='discrete', missing=0)
    ow.inputData(t)
    appl.exec_()
    ow.saveSettings()