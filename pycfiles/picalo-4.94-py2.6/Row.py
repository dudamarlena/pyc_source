# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/Row.py
# Compiled at: 2008-03-17 12:58:02
__rev_id__ = '$Id: Row.py,v 1.6 2005/08/11 08:53:48 rvk Exp $'
import BIFFRecords
from Deco import *
from Worksheet import Worksheet
import Style, Cell, ExcelFormula, datetime as dt

class Row(object):
    __slots__ = [
     '__init__',
     '__adjust_height',
     '__adjust_bound_col_idx',
     '__excel_date_dt',
     'get_height_in_pixels',
     'set_style',
     'get_xf_index',
     'get_cells_count',
     'get_min_col',
     'get_max_col',
     'get_str_count',
     'get_row_biff_data',
     'get_cells_biff_data',
     'get_index',
     'write',
     'write_blanks',
     '__idx',
     '__parent',
     '__parent_wb',
     '__cells',
     '__min_col_idx',
     '__max_col_idx',
     '__total_str',
     '__xf_index',
     '__has_default_format',
     '__height_in_pixels',
     'height',
     'has_default_height',
     'level',
     'collapse',
     'hidden',
     'space_above',
     'space_below']

    def __init__(self, index, parent_sheet):
        self.__idx = index
        self.__parent = parent_sheet
        self.__parent_wb = parent_sheet.get_parent()
        self.__cells = []
        self.__min_col_idx = 0
        self.__max_col_idx = 0
        self.__total_str = 0
        self.__xf_index = 15
        self.__has_default_format = 0
        self.__height_in_pixels = 17
        self.height = 255
        self.has_default_height = 0
        self.level = 0
        self.collapse = 0
        self.hidden = 0
        self.space_above = 0
        self.space_below = 0

    def __adjust_height(self, style):
        twips = style.font.height
        points = float(twips) / 20.0
        pix = int(round(points * 83.0 / 50.0 + 2.0 / 5.0))
        if pix > self.__height_in_pixels:
            self.__height_in_pixels = pix

    def __adjust_bound_col_idx(self, *args):
        for arg in args:
            if arg < self.__min_col_idx:
                self.__min_col_idx = arg
            elif arg > self.__max_col_idx:
                self.__max_col_idx = arg

    def __excel_date_dt(self, date):
        if isinstance(date, dt.date) and not isinstance(date, dt.datetime):
            epoch = dt.date(1899, 12, 31)
        elif isinstance(date, dt.time):
            date = dt.datetime.combine(dt.datetime(1900, 1, 1), date)
            epoch = dt.datetime(1900, 1, 1, 0, 0, 0)
        else:
            epoch = dt.datetime(1899, 12, 31, 0, 0, 0)
        delta = date - epoch
        xldate = delta.days + float(delta.seconds) / 86400
        if xldate > 59:
            xldate += 1
        return xldate

    def get_height_in_pixels(self):
        return self.__height_in_pixels

    @accepts(object, Style.XFStyle)
    def set_style(self, style):
        self.__adjust_height(style)
        self.__xf_index = self.__parent_wb.add_style(style)

    def get_xf_index(self):
        return self.__xf_index

    def get_cells_count(self):
        return len(self.__cells)

    def get_min_col(self):
        return self.__min_col_idx

    def get_max_col(self):
        return self.__min_col_idx

    def get_str_count(self):
        return self.__total_str

    def get_row_biff_data(self):
        height_options = self.height & 32767
        height_options |= (self.has_default_height & 1) << 15
        options = (self.level & 7) << 0
        options |= (self.collapse & 1) << 4
        options |= (self.hidden & 1) << 5
        options |= 0
        options |= 256
        if self.__xf_index != 15:
            options |= 128
        else:
            options |= 0
        options |= (self.__xf_index & 4095) << 16
        options |= (0 & self.space_above) << 28
        options |= (0 & self.space_below) << 29
        return BIFFRecords.RowRecord(self.__idx, self.__min_col_idx, self.__max_col_idx, height_options, options).get()

    def get_cells_biff_data(self):
        return ('').join([ cell.get_biff_data() for cell in self.__cells ])

    def get_index(self):
        return self.__idx

    @accepts(object, int, (str, unicode, int, float, dt.datetime, dt.time, dt.date, ExcelFormula.Formula), Style.XFStyle)
    def write(self, col, label, style):
        self.__adjust_height(style)
        self.__adjust_bound_col_idx(col)
        if isinstance(label, (str, unicode)):
            if len(label) > 0:
                self.__cells.extend([Cell.StrCell(self, col, self.__parent_wb.add_style(style), self.__parent_wb.add_str(label))])
                self.__total_str += 1
            else:
                self.__cells.extend([Cell.BlankCell(self, col, self.__parent_wb.add_style(style))])
        elif isinstance(label, (int, float)):
            self.__cells.extend([Cell.NumberCell(self, col, self.__parent_wb.add_style(style), label)])
        elif isinstance(label, (dt.datetime, dt.time)):
            self.__cells.extend([Cell.NumberCell(self, col, self.__parent_wb.add_style(style), self.__excel_date_dt(label))])
        else:
            self.__cells.extend([Cell.FormulaCell(self, col, self.__parent_wb.add_style(style), label)])

    @accepts(object, int, int, Style.XFStyle)
    def write_blanks(self, c1, c2, style):
        self.__adjust_height(style)
        self.__adjust_bound_col_idx(c1, c2)
        self.__cells.extend([Cell.MulBlankCell(self, c1, c2, self.__parent_wb.add_style(style))])