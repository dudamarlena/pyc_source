# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/xls_format.py
# Compiled at: 2012-10-12 07:02:39
import StringIO
from lxml import etree
from xlrd import open_workbook
from xlwt import Workbook, easyxf
from format import COILS_FORMAT_DESCRIPTION_OK, COILS_FORMAT_DESCRIPTION_INCOMPLETE, Format
from exception import RecordFormatException

class SimpleXLSFormat(Format):

    def __init__(self):
        Format.__init__(self)
        self._styles = None
        return

    def set_description(self, fd):
        code = Format.set_description(self, fd)
        if code[0] == 0:
            self.description = fd
            self._definition = self.description.get('data')
            for field in self.description['data']['columns']:
                if 'kind' not in field:
                    field['kind'] = 'string'

            self._discard_on_error = self._definition.get('discardMalformedRecords', False)
            return (
             COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return code

    @property
    def mimetype(self):
        return 'application/vnd.ms-excel'

    def process_in(self, rfile, wfile):
        self._sheet_num = int(self.description.get('sheet', '0'))
        self._book = open_workbook(file_contents=rfile.read())
        self._sheet = self._book.sheet_by_index(self._sheet_num)
        self._datetype = self._book.datemode
        wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        wfile.write(('<ResultSet formatName="{0}" className="{1}" tableName="{2}">').format(self.description.get('name'), self.__class__.__name__, self.description.get('tableName', '_undefined_')))
        row = []
        self._column_names = []
        for colx in range(self._sheet.ncols):
            self._column_names.append(self._sheet.cell_value(rowx=0, colx=colx))

        for self._rowNum in range(1, self._sheet.nrows):
            try:
                data = self.process_record_in()
                self.pause(self._rowNum)
            except RecordFormatException, e:
                self.log.warn(('Record format exception on row {0} column {1}: {2}').format(self._rowNum + 1, self._colNum + 1, e))
                if self._discard_on_error:
                    self.log.info(('Row {0} of input message dropped due to format error').format(self._rowNum + 1))
                else:
                    raise e
            else:
                if data is not None:
                    try:
                        wfile.write(data)
                    except UnicodeEncodeError, e:
                        raise e

        wfile.write('</ResultSet>')
        return

    def init_styles(self):
        self._styles = {}
        source = self._definition.get('styles', [])
        for style in source:
            descriptor = ('font:{0};alignment:{1};pattern:{2}').format(source[style].get('font', ''), source[style].get('alignment', ''), source[style].get('pattern', ''))
            format = source[style].get('format', None)
            if format is None:
                self._styles[style] = easyxf(descriptor)
            else:
                self._styles[style] = easyxf(descriptor, num_format_str=format)

        return

    def begin_output(self):
        if self._styles is None:
            self.init_styles()
        self._book = Workbook(style_compression=2)
        self._sheet = self._book.add_sheet('Sheet 1')
        if 'header' in self._definition:
            self._sheet.header_str = self._definition.get('header')
        if 'footer' in self._definition:
            self._sheet.footer_str = self._definition.get('footer')
        if 'portrait' in self._definition:
            if self._definition.get('portrait'):
                self._sheet.portrait = True
            else:
                self._sheet.portrait = False
        counter = 0
        style = self._styles.get('_title')
        for column in self._definition.get('columns'):
            if style is None:
                self._sheet.row(0).write(counter, column.get('title'))
            else:
                self._sheet.row(0).write(counter, column.get('title'), style)
            self._sheet.col(counter).width = int(column.get('width'))
            counter = counter + 1

        self._sheet.set_panes_frozen(True)
        self._sheet.set_horz_split_pos(1)
        return

    def end_output(self):
        pass

    def process_out(self, rfile, wfile):
        doc = etree.parse(rfile)
        self.begin_output()
        self._row = 1
        for record in doc.xpath('/ResultSet/row'):
            self.process_record_out(record)
            self._row = self._row + 1

        self.end_output()
        self._book.save(wfile)
        self._book = None
        return

    def process_record_out(self, record):
        self._column = 0
        for column in self._definition.get('columns'):
            value = record.xpath(('{0}[1]/text()').format(column.get('name')))
            if len(value) > 0:
                value = value[0]
            else:
                value = None
            kind = column.get('kind', 'string')
            style = column.get('style', None)
            if style is not None:
                style = self._styles.get(style, None)
            if kind == 'float':
                if value is None:
                    value = column.get('default', 0.0)
                if style is None:
                    self._sheet.row(self._row).write(self._column, float(value))
                else:
                    self._sheet.row(self._row).write(self._column, float(value), style)
            elif kind == 'integer':
                if value is None:
                    value = column.get('default', 0)
                if style is None:
                    self._sheet.row(self._row).write(self._column, int(value))
                else:
                    self._sheet.row(self._row).write(self._column, int(value), style)
            else:
                if value is not None:
                    value = self.decode_text(value)
                if style is None:
                    self._sheet.row(self._row).write(self._column, value)
                else:
                    self._sheet.row(self._row).write(self._column, value, style)
            self._column = self._column + 1

        self._sheet.flush_row_data()
        return