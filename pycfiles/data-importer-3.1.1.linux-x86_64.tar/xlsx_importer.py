# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/importers/xlsx_importer.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
from data_importer.importers.base import BaseImporter
from data_importer.readers.xlsx_reader import XLSXReader

class XLSXImporter(BaseImporter):

    def set_reader(self, data_only=True):
        """Read XLSX files"""
        self._reader = XLSXReader(self, data_only=True)