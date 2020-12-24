# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/git_additions/exporter/csv_exporter.py
# Compiled at: 2018-02-13 13:35:00
import csv, os

class CSVExporter(object):

    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def set_lines(self, lines):
        self.lines = lines

    def write_content(self, file_path):
        if not file_path.startswith('/'):
            file_path = '%s/%s' % (os.getcwd(), file_path)
        with open(file_path, 'w+') as (csv_file):
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for line in self.lines:
                wr.writerow(line)