# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/pdf.py
# Compiled at: 2009-10-07 18:08:46
"""PDF reporting using ReportLab's PDF library"""
from base import BaseReporter

class PdfReporter(BaseReporter):
    __module__ = __name__

    def __init__(self, filename):
        BaseReporter.__init__(self)
        from reportlab.platypus import XPreformatted, Spacer
        self.filename = filename
        self.lst = []
        self.lst.append(XPreformatted('<b><i><font size=20>Summary of test results</font></i></b>', self._normal_style()))
        self.lst.append(Spacer(0, 20))
        self.test_data = [
         (
          'Name', 'Result', 'Info')]

    def _normal_style(self):
        from reportlab.lib.styles import getSampleStyleSheet
        return getSampleStyleSheet()['Normal']

    def addSuccess(self, test_info):
        BaseReporter.addSuccess(self, test_info)
        self.test_data.append((str(test_info), 'Success', ''))

    def addError(self, test_info, err_info):
        BaseReporter.addError(self, test_info, err_info)
        self._add_unsuccessful_testcase('error', test_info, err_info)

    def addFailure(self, test_info, err_info):
        BaseReporter.addFailure(self, test_info, err_info)
        self._add_unsuccessful_testcase('failure', test_info, err_info)

    def _add_unsuccessful_testcase(self, failure_type, test_info, err_info):
        self.test_data.append((str(test_info), failure_type, str(err_info)))

    def done(self):
        BaseReporter.done(self)
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        table = Table(self.test_data)
        table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
        for i in xrange(1, len(self.test_data)):
            if self.test_data[i][1] == 'Success':
                color = colors.green
            else:
                color = colors.red
            table.setStyle(TableStyle([('TEXTCOLOR', (1, i), (1, i), color)]))

        self.lst.append(table)
        if self.cover_amount != None:
            self._print_coverage(self.cover_amount, self.coverage)
        SimpleDocTemplate(self.filename).build(self.lst)
        return

    def _print_coverage(self, amount, coverage):
        from reportlab.lib import colors
        from reportlab.platypus import Table, TableStyle, XPreformatted, Spacer
        self.lst.append(Spacer(0, 20))
        self.lst.append(XPreformatted('<b><i><font size=20>Coverage information</font></i></b>\n\nCovered %3.2f%% of the code.' % coverage.total_coverage_percentage(), self._normal_style()))
        if amount != 'slim':
            self.lst.append(Spacer(0, 20))
            data = [('Lines', 'Covered lines', 'Percentage', 'Module', 'Path')]
            modname = coverage.modname
            for (filename, stats) in coverage.getstatistics().items():
                data.append((str(stats['lines']), str(stats['covered']), str(stats['percent']) + '%', modname(filename), filename))

            data.append((str(coverage.total_lines()), str(coverage.total_lines_covered()), str(coverage.total_coverage_percentage()) + '%', 'TOTAL', ''))
            table = Table(data)
            table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
            self.lst.append(table)