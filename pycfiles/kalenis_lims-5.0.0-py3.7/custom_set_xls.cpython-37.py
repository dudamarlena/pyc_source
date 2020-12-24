# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_instrument_custom_set/custom_set_xls.py
# Compiled at: 2019-01-16 09:41:20
# Size of source mod 2**32: 5349 bytes
import io, xlrd
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.lims.formula_parser import FormulaParser
IGNORE_SHEET = '###'
ANALYSIS_CODE = 'Analysis Code'
DATA_HEADER = 'Data Header'
FORMULA = 'Formula'

def getControllerName():
    if Transaction().language in ('es', 'es_419'):
        return 'Planilla personalizada - XLS'
    return 'Custom Set - XLS'


def parse(self, infile):
    LabWorkYear = Pool().get('lims.lab.workyear')
    filedata = io.StringIO(infile)
    workbook = xlrd.open_workbook(file_contents=(filedata.getvalue()))
    worksheets = workbook.sheet_names()
    for worksheet_name in worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        if worksheet.cell_value(0, 0) == IGNORE_SHEET:
            continue
        self.analysis_code = None
        self.formula = None
        self.header = []
        num_rows = worksheet.nrows - 1
        curr_row = -1
        header_found = False
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            if not self.analysis_code:
                self.getAnalysisCode(row)
            if not self.formula:
                self.getFormula(row)
            if not self.header:
                curr_row += self.getDataHeader(worksheet, curr_row)
            if self.analysis_code:
                if self.formula and self.header:
                    row = [cell for cell in row if cell.ctype != xlrd.XL_CELL_EMPTY]
                    row = row[:len(self.header)]
                    if header_found is False:
                        row = [cell.value for cell in row]
                        if row == self.header:
                            header_found = True
                            continue
                for cell in row:
                    if cell.ctype != xlrd.XL_CELL_NUMBER:
                        header_found = False
                        continue

                row = [cell.value for cell in row]
                if len(row) < len(self.header):
                    header_found = False
                    continue
            workyear = LabWorkYear.search([
             'code', '=', str(int(row[1]))])
            padding = None
            if workyear:
                if workyear[0]:
                    if workyear[0].sample_sequence:
                        padding = workyear[0].sample_sequence.padding
            if padding:
                sample = '%%0%sd' % padding % int(row[0])
                fraction = str(int(row[1])) + '/' + sample + '-' + str(int(row[2]))
                repetition = int(row[3])
                values = {}
                remaining_header = self.header[4:]
                i = 4
                for h in remaining_header:
                    h = ''.join(h.split())
                    h = ''.join(h.split('.'))
                    values[h] = row[i]
                    i += 1

                formulaParser = FormulaParser(self.formula, values)
                values['result'] = formulaParser.getValue()
                values['row_number'] = curr_row + 1
                if fraction in self.rawresults:
                    if self.analysis_code in self.rawresults[fraction]:
                        self.rawresults[fraction][self.analysis_code][repetition] = values
                    else:
                        self.rawresults[fraction][self.analysis_code] = {repetition: values}
                else:
                    self.rawresults[fraction] = {self.analysis_code: {repetition: values}}


def getAnalysisCode(self, row):
    found = False
    for cell in row:
        if found:
            if cell.ctype == xlrd.XL_CELL_TEXT:
                self.analysis_code = cell.value
                return
        if cell.value == ANALYSIS_CODE:
            found = True


def getDataHeader(self, worksheet, curr_row):
    row = worksheet.row(curr_row)
    for cell in row:
        if cell.value == DATA_HEADER:
            curr_row += 1
            if curr_row < worksheet.nrows - 1:
                next_row = worksheet.row(curr_row)
                for c in next_row:
                    if c.ctype == xlrd.XL_CELL_TEXT:
                        self.header.append(c.value)

                return 1
        return 0


def getFormula(self, row):
    found = False
    for cell in row:
        if found:
            if cell.ctype == xlrd.XL_CELL_TEXT:
                value = ''.join(cell.value.split())
                self.formula = ''.join(value.split('.'))
                return
        if cell.value == FORMULA:
            found = True