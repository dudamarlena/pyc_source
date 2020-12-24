# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/writer/writer.py
# Compiled at: 2014-10-06 17:20:58
from ..exceptions import WriterProcessingIncompleteError

class Writer(object):
    suffix = 'ext'

    def __init__(self):
        self.OutputFilesClass = None
        self.galaxy_override = False
        self.data = None
        self.processed_data = None
        self.processing_complete = False
        self.used_filenames = []
        self.name = None
        return

    def process(self):
        self.processed_data = self.data
        self.processing_complete = True

    def write(self):
        if self.processing_complete:
            self.OutputFilesClass.extension = self.suffix
            next_output_file = self.OutputFilesClass.get_next_file()
            self.used_filenames.append(next_output_file)
            with open(next_output_file, 'w') as (outfile):
                outfile.write(self.processed_data)
        else:
            raise WriterProcessingIncompleteError('Write called but processing was not marked as\n                            complete. Not writing')

    def get_name(self):
        return self.OutputFilesClass._get_filename()