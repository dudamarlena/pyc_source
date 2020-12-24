# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/SourceProcessors/WebAdminResults.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 1795 bytes
"""
    Processor for a CSV file output from WebAdmin.
    Store the required column names and their parameter names here.
    (Parameters are for Routine AddDRS
    The required columns must be present: this class
    returns the vector of their orders
     """
from typing import Dict
import csv

class WebAdminResults:

    def __init__(self, column_dict: dict):
        self.column_dict = column_dict

    def extract_data(self, text_line: str) -> object:
        """
        Creates a parameter dictionary of key:parameter_name, value:parameter_value
        :type text_line: str
        :param text_line:
        :return:
        """
        text_line = text_line.rstrip('\n')
        line_beads = text_line.split(self.sep)
        if len(line_beads) < len(self.required_columns):
            raise ValueError('not enough data: ' + text_line)
        rc = {}
        for k, v in self.column_parameters.items():
            rc[v] = line_beads[self.required_columns[k]]

        return rc

    def csv_to_dict(self, file_name: str) -> Dict[(str, str)]:
        rc = []
        with open(file_name, newline='\n', encoding='utf-8') as (csvfile):
            rdr = csv.DictReader(csvfile, dialect='unix')
            for row in rdr:
                db_parms = {}
                for k, v in self.column_dict.items():
                    db_parms[v] = row[k]

                rc.append(db_parms)

        return rc