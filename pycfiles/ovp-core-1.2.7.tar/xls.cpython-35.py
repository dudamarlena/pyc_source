# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/helpers/xls.py
# Compiled at: 2017-06-13 14:16:15
# Size of source mod 2**32: 556 bytes
from io import BytesIO
from datetime import datetime
from pyexcel_xls import save_data
from django.http import HttpResponse

def Response(rows, filename=None, sheet_name='root'):
    if filename is None:
        filename = 'data-export-{}.xls'.format(datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    xls_buffer = BytesIO()
    save_data(xls_buffer, {str(sheet_name): rows})
    response = HttpResponse(xls_buffer.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response