# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/importers/generic.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
from data_importer.readers.xls_reader import XLSReader
from data_importer.readers.xlsx_reader import XLSXReader
from data_importer.readers.csv_reader import CSVReader
from data_importer.readers.xml_reader import XMLReader
from data_importer.core.exceptions import UnsuportedFile
from .base import BaseImporter

class GenericImporter(BaseImporter):
    """
    An implementation of BaseImporter that sets the right reader
    by file extension.
    Probably the best choice for almost all implementation cases
    """

    def set_reader(self):
        reader = self.get_reader_class()
        extra_values = {b'xlsx': {b'data_only': True}, b'xls': {b'sheet_name': self.Meta.sheet_name or None, b'sheet_index': self.Meta.sheet_index or 0}, 
           b'csv': {b'delimiter': self.Meta.delimiter or b';'}, b'xml': {}}
        selected_extra_values = extra_values[self.get_source_file_extension()]
        self._reader = reader(self, **selected_extra_values)
        return

    def get_reader_class(self):
        """
        Gets the right file reader class by source file extension
        """
        readers = {b'xls': XLSReader, 
           b'xlsx': XLSXReader, 
           b'xml': XMLReader, 
           b'csv': CSVReader}
        source_file_extension = self.get_source_file_extension()
        if source_file_extension not in readers.keys():
            raise UnsuportedFile(b'Unsuported File')
        return readers[source_file_extension]

    def get_source_file_extension(self):
        """
        Gets the source file extension. Used to choose the right reader
        """
        if hasattr(self.source, b'file') and hasattr(self.source.file, b'name'):
            filename = self.source.file.name
        elif hasattr(self.source, b'file_upload'):
            if hasattr(self.source.file_upload, b'name'):
                filename = self.source.file_upload.name
            else:
                filename = self.source.file_upload
        elif hasattr(self.source, b'name'):
            filename = self.source.name
        else:
            filename = self.source
        ext = filename.split(b'.')[(-1)]
        return ext.lower()