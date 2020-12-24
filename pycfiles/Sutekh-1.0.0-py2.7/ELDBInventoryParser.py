# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/ELDBInventoryParser.py
# Compiled at: 2019-12-11 16:37:58
"""Parser for ELDB inventory format"""
import re
from sutekh.core.ELDBUtilities import gen_name_lookups
from sutekh.base.io.IOBase import BaseLineParser

class ELDBInventoryParser(BaseLineParser):
    """Parser for the ELDB Inventory format.

       The inventory file has no name info, so the holder name isn't changed
       by the parser."""
    _oCardRe = re.compile('\\s*"(?P<name>[^"]*)"\\s*,\\s*(?P<cnt>[0-9]+)')

    def __init__(self):
        super(ELDBInventoryParser, self).__init__()
        self._dNameCache = gen_name_lookups()

    def _feed(self, sLine, oHolder):
        """Handle line by line data"""
        if sLine.startswith('"ELDB - Inv'):
            return
        else:
            oMatch = self._oCardRe.match(sLine)
            if oMatch:
                iCnt = int(oMatch.group('cnt'))
                sName = oMatch.group('name').strip()
                if sName in self._dNameCache:
                    sName = self._dNameCache[sName]
                if iCnt:
                    oHolder.add(iCnt, sName, None, None)
            return