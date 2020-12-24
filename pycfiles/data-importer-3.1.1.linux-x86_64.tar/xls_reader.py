# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/readers/xls_reader.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
import datetime, xlrd
from django.db.models.fields.files import FieldFile

class XLSReader(object):

    def __init__(self, instance, sheet_name=None, sheet_index=0, on_demand=True):
        if isinstance(instance.source, FieldFile):
            source = instance.source.path
        else:
            source = instance.source
        self.workbook = xlrd.open_workbook(source, on_demand=on_demand)
        if sheet_name:
            self.worksheet = self.workbook.sheet_by_name(instance.Meta.sheet_name)
        else:
            self.worksheet = self.workbook.sheet_by_index(sheet_index)

    @staticmethod
    def convert_value(item, workbook):
        """
        Handle different value types for XLS. Item is a cell object.
        """
        if item.ctype == 3:
            return datetime.datetime(*xlrd.xldate_as_tuple(item.value, workbook.datemode))
        if item.ctype == 2:
            if item.value % 1 == 0:
                return int(item.value)
            else:
                return item.value

        return item.value

    def read(self):
        for i in range(0, self.worksheet.nrows):
            values = [ self.convert_value(cell, self.workbook) for cell in self.worksheet.row(i) ]
            yield values