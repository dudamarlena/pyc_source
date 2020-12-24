# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jsonmapper\renderers.py
# Compiled at: 2012-04-14 19:39:17
from cStringIO import StringIO
import csv

class CSVRenderer(object):

    def __init__(self, info):
        pass

    def __call__(self, value, system):
        fout = StringIO()
        writer = csv.writer(fout, delimiter=value.get('delimiter', ';'), quoting=csv.QUOTE_ALL)
        writer.writerow(value['header'])
        writer.writerows(value['rows'])
        resp = system['request'].response
        resp.content_type = 'text/csv'
        resp.content_disposition = ('attachment;filename="{}"').format(value['filename'])
        return fout.getvalue()