# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/LookupCSVParser.py
# Compiled at: 2019-12-11 16:37:52
"""Parse data into the lookup from a CSV file.

   The CSV file is formatted as:
   Domain,Lookup Name,Desired Name."""
import csv
from logging import Logger
from ..core.BaseTables import LookupHints

class LookupCSVParser(object):
    """Parse lookup info from a CSV file and add the required
       LookupHints entries to the database."""

    def __init__(self, oLogHandler):
        self.oLogger = Logger('lookup data parser')
        if oLogHandler is not None:
            self.oLogger.addHandler(oLogHandler)
        self.oLogHandler = oLogHandler
        return

    def parse(self, fIn):
        """Process the CSV file line into the CardSetHolder"""
        oCsvFile = csv.reader(fIn)
        aRows = list(oCsvFile)
        if hasattr(self.oLogHandler, 'set_total'):
            self.oLogHandler.set_total(len(aRows))
        for sDomain, sLookup, sValue in aRows:
            oLookup = LookupHints(domain=sDomain, lookup=sLookup, value=sValue)
            oLookup.syncUpdate()
            self.oLogger.info('Added Lookup : (%s, %s)', sDomain, sLookup)