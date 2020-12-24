# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\export_models\export_document_elements.py
# Compiled at: 2019-01-28 08:23:10
# Size of source mod 2**32: 6175 bytes
from enum import Enum
import logging

class ExportDocumentElementTypesCollection(Enum):
    ROW = 0
    TABLE = 1
    STATIC_ROW = 2
    EMPTY_ROW = 3


class ExportCellValueConvert(Enum):
    NO_CONVERT = 0
    EXTRACT_DATE = 1
    THOUSAND_FORMAT = 2
    CLEAR_NOT_NUMBER = 3
    MONEY_FORMAT = 4


class ExportElementStyle:

    def __init__(self, bgc='#ffffff', color='#000000', ta='left', fz='8', fm='', fw='normal', fs='normal', u='', ff='arial', width=50, row=-1):
        try:
            if bgc != '#ffffff':
                t = 0
            self.width = width
            self.bgc = bgc
            self.color = color
            self.ta = ta
            self.fz = fz
            self.fm = fm
            self.fw = fw
            self.fs = fs
            self.u = u
            self.ff = ff
            if row > 0:
                self.bls = 'solid'
                self.brs = 'solid'
                self.bts = 'solid'
                self.bbs = 'solid'
                self.blc = '#7f7f7f'
                self.brc = '#7f7f7f'
                self.btc = '#7f7f7f'
                self.bbc = '#7f7f7f'
                self.blt = 'solid'
                self.brt = 'solid'
                self.btt = 'solid'
                self.bbt = 'solid'
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ExportDocumentElementCell:

    def __init__(self, navigate_param):
        try:
            self.value_attribute = navigate_param.value_attribute
            self.paths = []
            for path in navigate_param.paths:
                self.paths.append(path)

            self.convert_types = []
            for convert_type in navigate_param.convert_types:
                self.convert_types.append(ExportCellValueConvert(convert_type))

            self.style = navigate_param.style
            self.value = ''
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def set_cell_value(self, value):
        try:
            self.value = value
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def set_cell_style(self, bgc='#ffffff', color='#000000', ta='left', fz='8', fm='', fw='normal', fs='normal', u='', ff='arial', width=50, row=-1):
        try:
            self.style = ExportElementStyle(bgc=bgc, color=color, ta=ta, fz=fz, fm=fm, fw=fw, fs=fs, u='', ff=ff, width=width,
              row=row)
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ExportDocumentElementRow:

    def __init__(self):
        try:
            self.index = -1
            self.cells = []
            self.style = None
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def set_row_style(self, bgc='#ffffff', color='#000000', ta='left', fz='10', fm='', fw='normal', fs='normal', u='', ff='arial', width=50, row=-1):
        try:
            self.style = ExportElementStyle(bgc=bgc, color=color, ta=ta, fz=fz, fm=fm, fw=fw, fs=fs, u='', ff=ff, width=width,
              row=row)
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def set_row_cells_style(self):
        try:
            for cell in self.cells:
                cell.set_cell_style(bgc=(self.style.bgc), color=(self.style.color), ta=(self.style.ta), fz=(self.style.fz), fm=(self.style.fm), fw=(self.style.fw), fs=(self.style.fs), u=(self.style.u), ff=(self.style.ff),
                  width=(self.style.width),
                  row=(-1))

        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_value_cells(self, navigate_params, values):
        try:
            for value in values:
                self.cells.append(ExportDocumentElementCell(navigate_params))
                last_cell = self.cells[(len(self.cells) - 1)]
                last_cell.set_cell_value(value)

        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ExportDocumentElementTable:

    def __init__(self, source_path):
        try:
            self.source_path = source_path
            self.header_row = None
            self.header_source = None
            self.rows = []
            self.rows_source = None
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ExportDocumentElement:

    def __init__(self, type_id, name, title=''):
        try:
            self.type = ExportDocumentElementTypesCollection(type_id)
            self.name = name
            self.title = title
            self.table = None
            self.row = None
            self.include_in_report = True
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_element_table(self, navigate_params):
        try:
            pass
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_element_row(self, navigate_params):
        try:
            self.row = ExportDocumentElementRow()
            for navigate_param in navigate_params:
                self.row.cells.append(ExportDocumentElementCell(navigate_param))

        except Exception as e:
            logging.error('Error initialization. ' + str(e))