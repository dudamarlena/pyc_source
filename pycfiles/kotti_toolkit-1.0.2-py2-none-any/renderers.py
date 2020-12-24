# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_toolkit/kotti_toolkit/renderers.py
# Compiled at: 2018-09-18 23:53:45
import os, csv, StringIO

class CSVRenderer(object):

    def __init__(self, info):
        pass

    def __call__(self, value, system):
        resp = system['request'].response
        resp.content_type = 'text/csv'
        resp.content_disposition = 'attachment;filename="report.csv"'
        if type(value) == str:
            return value
        formatted_output = StringIO.StringIO()
        writer = csv.writer(formatted_output, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(value['header'])
        writer.writerows(value['rows'])
        return formatted_output.getvalue()