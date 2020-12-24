# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/helpers/csv.py
# Compiled at: 2017-06-13 14:16:15
# Size of source mod 2**32: 478 bytes
import csv
from datetime import datetime
from django.http import HttpResponse

def Response(rows, filename=None, sheet_name=None):
    if filename is None:
        filename = 'data-export-{}.csv'.format(datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    csv_writer = csv.writer(response)
    for row in rows:
        csv_writer.writerow(row)

    return response