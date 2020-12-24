# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/readers/csv_reader.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
import csv

class CSVReader(object):

    def __init__(self, instance, delimiter=b';'):
        self.instance = instance
        self.delimiter = delimiter

    def read(self):
        return csv.reader(self.instance.source, delimiter=self.delimiter)