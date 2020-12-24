# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\export_models\export_document_report_model.py
# Compiled at: 2019-01-28 06:53:02
# Size of source mod 2**32: 3541 bytes
import json, uuid, logging

class ExportDocumentReportCellContent:

    def __init__(self, data, bgc='#ffffff', color='#000000', ta='left', fz='10', fm='', fw='normal', fs='normal', u='', ff='arial', width=50, id=-1, row=-1, show_grid=False, contains_data=False, height=30):
        try:
            self.width = width
            self.data = data
            self.bgc = bgc
            self.color = color
            self.ta = ta
            self.fz = fz
            self.fm = fm
            self.fw = fw
            self.fs = fs
            self.u = u
            self.ff = ff
            self.id = id
            self.ww = 'break-word'
            self.ws = 'pre-line'
            self.va = 'middle'
            self.ta = 'center'
            self.height = height
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


class ExportDocumentReportCell:

    def __init__(self, sheet, row, col, cellJson):
        try:
            self.sheet = sheet
            self.row = row
            self.col = col
            self.json = cellJson
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ExportDocumentGroup:

    def __init__(self, level, span):
        try:
            self.level = level
            self.span = span
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def toJSON(self):
        return json.dumps(self, default=(lambda o: o.__dict__), sort_keys=True,
          indent=4)


class ExportDocumentReportFloatings:

    def __init__(self, sheet, name, ftype, json):
        self.sheet = sheet
        self.name = name
        self.ftype = ftype
        self.json = json


class ExportDocumentReportSheet:

    def __init__(self, id, name):
        try:
            self.id = id
            self.name = name
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ExportDocumentReportModel:

    def __init__(self, fileName):
        try:
            self.fileName = fileName
            self.sheets = []
            self.floatings = []
            self.cells = []
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def add_sheet(self, id, name):
        try:
            self.sheets.append(ExportDocumentReportSheet(id, name))
        except Exception as e:
            logging.error('Error ' + str(e))

    def toJSON(self):
        return json.dumps(self, default=(lambda o: o.__dict__), sort_keys=True,
          indent=4)