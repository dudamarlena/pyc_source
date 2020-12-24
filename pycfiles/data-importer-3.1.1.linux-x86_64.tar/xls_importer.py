# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/importers/xls_importer.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
from .base import BaseImporter
from data_importer.readers import XLSReader

class XLSImporter(BaseImporter):

    def set_reader(self):
        """
            [[1,2,3], [2,3,4]]
        """
        sheet_by_name = self.Meta.sheet_name or None
        sheet_by_index = self.Meta.sheet_index or 0
        self._reader = XLSReader(self, sheet_name=sheet_by_name, sheet_index=sheet_by_index)
        return