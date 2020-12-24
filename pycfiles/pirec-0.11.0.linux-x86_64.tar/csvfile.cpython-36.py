# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/recorders/csvfile.py
# Compiled at: 2017-02-10 11:03:57
# Size of source mod 2**32: 1164 bytes
"""Exposes the CSVFile result recorder."""
import os, csv

class CSVFile(object):
    __doc__ = 'Records results to a CSV file.\n\n    Args:\n        path (str): The file to which results should be written\n        values (dict): a mapping from table columns to values\n    '

    def __init__(self, path, values):
        """Initialize the recorder."""
        self.path = path
        self.values = values

    def write(self, results):
        """Write results to the file specified.

        Args:
            results (dict): A dictionary of results to record

        Note:
            If the specified does not exist it will be created and a
            header will be written , otherwise the new result is appended.

        """
        field_names = self.values.keys()
        write_header = not os.path.exists(self.path)
        with open(self.path, 'a') as (output_file):
            writer = csv.DictWriter(output_file, fieldnames=field_names)
            if write_header:
                writer.writeheader()
            row = {}
            for field in self.values:
                row[field] = self.values[field](results)

            writer.writerow(row)