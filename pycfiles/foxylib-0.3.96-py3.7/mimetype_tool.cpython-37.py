# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/file/mimetype_tool.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 877 bytes
from mimetypes import guess_type

class MimetypeTool:

    class Value:
        TEXT_XPYTHON = 'text/x-python'
        TEXT_PLAIN = 'text/plain'
        APPLICATION_XHWP = 'application/x-hwp'
        APPLICATION_MS_EXCEL = 'application/vnd.ms-excel'

    V = Value

    @classmethod
    def url2mimetype(cls, url):
        mimetype, encoding = guess_type(url)
        return mimetype

    @classmethod
    def mimetype2is_ms_excel(cls, mimetype):
        h = {'application/vnd.ms-excel',
         'application/msexcel',
         'application/x-msexcel',
         'application/x-ms-excel',
         'application/x-excel',
         'application/x-dos_ms_excel',
         'application/xls',
         'application/x-xls',
         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        return mimetype in h