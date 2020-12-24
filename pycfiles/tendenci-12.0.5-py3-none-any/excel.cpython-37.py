# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/model_report/exporters/excel.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 3343 bytes
from builtins import str
from xlwt import Workbook, easyxf
from django.http import HttpResponse
from tendenci.libs.model_report import arial10
from .base import Exporter

class FitSheetWrapper(object):
    __doc__ = "Try to fit columns to max size of any entry.\n    To use, wrap this around a worksheet returned from the\n    workbook's add_sheet method, like follows:\n\n        sheet = FitSheetWrapper(book.add_sheet(sheet_name))\n\n    The worksheet interface remains the same: this is a drop-in wrapper\n    for auto-sizing columns.\n    "

    def __init__(self, sheet):
        self.sheet = sheet
        self.widths = dict()
        self.heights = dict()

    def write(self, r, c, label='', *args, **kwargs):
        (self.sheet.write)(r, c, label, *args, **kwargs)
        self.sheet.row(r).collapse = True
        bold = False
        if args:
            style = args[0]
            bold = str(style.font.bold) in ('1', 'true', 'True')
        width = int(arial10.fitwidth(label, bold))
        if width > self.widths.get(c, 0):
            self.widths[c] = width
            self.sheet.col(c).width = width
        height = int(arial10.fitheight(label, bold))
        if height > self.heights.get(r, 0):
            self.heights[r] = height
            self.sheet.row(r).height = height

    def __getattr__(self, attr):
        return getattr(self.sheet, attr)


class ExcelExporter(Exporter):

    @classmethod
    def render(cls, report, column_labels, report_rows, report_inlines):
        book = Workbook(encoding='utf-8')
        sheet1 = FitSheetWrapper(book.add_sheet(report.get_title()[:20]))
        stylebold = easyxf('font: bold true; alignment:')
        stylevalue = easyxf('alignment: horizontal left, vertical top;')
        row_index = 0
        for index, x in enumerate(column_labels):
            sheet1.write(row_index, index, '%s' % x, stylebold)

        row_index += 1
        for g, rows in report_rows:
            if g:
                sheet1.write(row_index, 0, '%s' % g, stylebold)
                row_index += 1
            for row in list(rows):
                if row.is_value():
                    for index, x in enumerate(row):
                        if isinstance(x.value, (list, tuple)):
                            xvalue = ''.join(['%s\n' % v for v in x.value])
                        else:
                            xvalue = x.text()
                        sheet1.write(row_index, index, xvalue, stylevalue)

                    row_index += 1
                else:
                    if row.is_caption:
                        for index, x in enumerate(row):
                            if not isinstance(x, str):
                                sheet1.write(row_index, index, x.text(), stylebold)
                            else:
                                sheet1.write(row_index, index, x, stylebold)

                        row_index += 1

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % report.slug
        book.save(response)
        return response