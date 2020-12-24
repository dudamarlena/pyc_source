# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/actions.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 1626 bytes
from collections import defaultdict
from datetime import date
import tempfile
from zipfile import ZipFile
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from explorer.exporters import CSVExporter

def generate_report_action(description='Generate CSV file from SQL query'):

    def generate_report(modeladmin, request, queryset):
        results = [report for report in queryset if report.passes_blacklist()[0]]
        queries = len(results) > 0 and _package(results) or defaultdict(int)
        response = HttpResponse((queries['data']), content_type=(queries['content_type']))
        response['Content-Disposition'] = queries['filename']
        response['Content-Length'] = queries['length']
        return response

    generate_report.short_description = description
    return generate_report


def _package(queries):
    ret = {}
    is_one = len(queries) == 1
    name_root = lambda n: 'attachment; filename=%s' % n
    ret['content_type'] = is_one and 'text/csv' or 'application/zip'
    ret['filename'] = is_one and name_root('%s.csv' % queries[0].title.replace(',', '')) or name_root('Report_%s.zip' % date.today())
    ret['data'] = is_one and CSVExporter(queries[0]).get_output() or _build_zip(queries)
    ret['length'] = is_one and len(ret['data']) or ret['data'].blksize
    return ret


def _build_zip(queries):
    temp = tempfile.TemporaryFile()
    zip_file = ZipFile(temp, 'w')
    for r in queries:
        zip_file.writestr('%s.csv' % r.title, CSVExporter(r).get_output() or 'Error!')

    zip_file.close()
    ret = FileWrapper(temp)
    temp.seek(0)
    return ret