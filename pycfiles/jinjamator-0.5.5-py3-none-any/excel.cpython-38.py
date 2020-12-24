# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/file/excel.py
# Compiled at: 2020-04-25 16:12:43
# Size of source mod 2**32: 977 bytes
from jinjamator.tools.xlsx_tools import XLSXReader, XLSXWriter
import os

def load(path, **kwargs):
    if not os.path.isabs(path):
        path = os.path.join(self._parent.task_base_dir, path)
    xlsx = XLSXReader(path, kwargs.get('work_sheet_name', 'Sheet1'), kwargs.get('cache', True))
    xlsx.parse_header(kwargs.get('header_lines', 1))
    xlsx.parse_data()
    return xlsx.data