# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/writer/csv_w.py
# Compiled at: 2014-10-06 17:20:07
from writer import Writer
from ..exceptions import WriterProcessingIncompleteError
import csv

class CSV_W(Writer):
    suffix = 'csv'

    def process(self):
        self.processed_data = self.data
        self.processing_complete = True

    def write(self):
        if self.processing_complete:
            base_name = self.OutputFilesClass.given_filename
            if base_name is None:
                base_name = ''
            for sheet in self.processed_data:
                self.OutputFilesClass.given_filename = base_name + '.' + sheet
                self.OutputFilesClass.extension = 'csv'
                next_output_file = self.OutputFilesClass.get_next_file()
                self.used_filenames.append(next_output_file)
                with open(next_output_file, 'wb') as (csvfile):
                    tablewriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                    tablewriter.writerow(self.processed_data[sheet]['header'])
                    for row in self.processed_data[sheet]['data']:
                        tablewriter.writerow(row)

            self.OutputFilesClass.given_filename = base_name
        else:
            raise WriterProcessingIncompleteError('Write called but processing was not marked as complete. Not writing')
        return