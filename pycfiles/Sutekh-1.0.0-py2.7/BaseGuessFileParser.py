# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/BaseGuessFileParser.py
# Compiled at: 2019-12-11 16:37:52
"""Base class for a guessing file parser.

   Handles the logic around trying to parse the card set with multiple
   parsers.
   """
import StringIO
from ..core.CardSetHolder import CardSetHolder

class BaseGuessFileParser(object):
    """Parser which guesses the file type"""
    PARSERS = []

    def __init__(self):
        self.oChosenParser = None
        return

    def guess_format(self, oFile):
        """Handle the guessing"""
        for cParser in self.PARSERS:
            oHolder = CardSetHolder()
            oFile.seek(0)
            oParser = cParser()
            try:
                oParser.parse(oFile, oHolder)
            except IOError:
                continue

            if oHolder.num_entries == 0:
                continue
            return oParser

        return

    def parse(self, fIn, oHolder):
        """attempt arse a file into the given holder"""
        oCopy = StringIO.StringIO(fIn.read())
        self.oChosenParser = self.guess_format(oCopy)
        if not self.oChosenParser:
            raise IOError('Unable to identify the file format')
        oCopy.seek(0)
        self.oChosenParser.parse(oCopy, oHolder)