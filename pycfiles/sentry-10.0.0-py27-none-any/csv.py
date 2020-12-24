# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/mixins/csv.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import csv, six
from django.utils.encoding import force_bytes
from django.http import StreamingHttpResponse
if six.PY3:

    def encode_row(row):
        return row


else:

    def encode_row(row):
        return map(force_bytes, row)


class Echo(object):

    def write(self, value):
        return value


class CsvMixin(object):

    def get_header(self, **kwargs):
        return ()

    def get_row(self, item, **kwargs):
        return ()

    def to_csv_response(self, iterable, filename, **kwargs):

        def row_iter():
            header = self.get_header(**kwargs)
            if header:
                yield header
            for item in iterable:
                yield self.get_row(item, **kwargs)

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(encode_row(r)) for r in row_iter()), content_type='text/csv')
        response['Content-Disposition'] = ('attachment; filename="{}.csv"').format(filename)
        return response