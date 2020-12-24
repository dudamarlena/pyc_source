# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/model_report/exporters/pdf.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 1264 bytes
from io import BytesIO
from cgi import escape
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from .base import Exporter

class PdfExporter(Exporter):

    @classmethod
    def render(cls, report, column_labels, report_rows, report_inlines):
        setattr(report, 'is_export', True)
        context = {'report':report, 
         'column_labels':column_labels, 
         'report_rows':report_rows, 
         'report_inlines':report_inlines, 
         'pagesize':'legal landscape'}
        template = get_template('model_report/export_pdf.html')
        html = template.render(context=context)
        result = BytesIO()
        pdf_encoding = 'UTF-8'
        pdf = pisa.CreatePDF((BytesIO(html.encode(pdf_encoding))), result, encoding=pdf_encoding)
        if not pdf.err:
            response = HttpResponse((result.getvalue()), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s.pdf' % report.slug
        else:
            response = HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        result.close()
        return response