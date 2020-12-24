# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/CSVParser.py
# Compiled at: 2019-12-11 16:37:52
"""Parse cards from a CSV file."""
import csv

class CSVParser(object):
    """Parser cards from a CSV file into a CardSetHolder.

       Cards should be listed in columns and specify at least the card name and
       card count. Each row may optionally include the name of the expansion
       the card comes from.
       """

    def __init__(self, iCardNameColumn, iCountColumn, iExpansionColumn=None, bHasHeader=True):
        self.iCardNameColumn = iCardNameColumn
        self.oCS = None
        self.iCountColumn = iCountColumn
        self.iExpansionColumn = iExpansionColumn
        self.bHasHeader = bHasHeader
        return

    def _process_row(self, aRow):
        """Extract the relevant data from a single row in the CSV file."""
        sName = aRow[self.iCardNameColumn].strip()
        if not sName:
            return
        else:
            try:
                iCount = int(aRow[self.iCountColumn])
            except ValueError:
                iCount = 1
                self.oCS.add_warning("Count for '%s' could not be determined and was set to one." % (
                 sName,))

            if self.iExpansionColumn is not None:
                sExpansionName = aRow[self.iExpansionColumn].strip()
            else:
                sExpansionName = None
            self.oCS.add(iCount, sName, sExpansionName, None)
            return

    def parse(self, fIn, oHolder):
        """Process the CSV file line into the CardSetHolder"""
        oCsvFile = csv.reader(fIn)
        self.oCS = oHolder
        oIter = iter(oCsvFile)
        if self.bHasHeader:
            oIter.next()
        for aRow in oIter:
            try:
                self._process_row(aRow)
            except ValueError as oExp:
                raise ValueError('Line %d in CSV file could not be parsed (%s)' % (
                 oCsvFile.line_num, oExp))