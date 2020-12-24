# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/importers/xml_importer.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
from data_importer.importers.base import BaseImporter
from data_importer.readers.xml_reader import XMLReader

class XMLImporter(BaseImporter):
    """
    Import XML files
    """
    root = b'root'

    def set_reader(self):
        self._reader = XMLReader(self)