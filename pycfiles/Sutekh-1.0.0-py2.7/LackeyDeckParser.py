# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/LackeyDeckParser.py
# Compiled at: 2019-12-11 16:37:57
"""Parser for Lackey CCG deck format"""
import string
from sutekh.base.core.BaseTables import AbstractCard
from sutekh.io.WriteLackeyCCG import lackey_name
from sutekh.base.io.IOBase import BaseLineParser

def gen_name_lookups():
    """Create a lookup table to map Lackey CCG names to Sutekh names -
       reduces the number of user queries"""
    dNameCache = {}
    for oCard in AbstractCard.select():
        sSutekhName = oCard.name
        sLackeyName = lackey_name(oCard)
        if sLackeyName != sSutekhName:
            dNameCache[sLackeyName] = sSutekhName

    return dNameCache


class LackeyDeckParser(BaseLineParser):
    """Parser for the Lackey Deck format."""

    def __init__(self):
        super(LackeyDeckParser, self).__init__()
        self._dNameCache = gen_name_lookups()

    def _feed(self, sLine, oHolder):
        """Read the line into the given CardSetHolder"""
        if sLine[0] in string.digits:
            sNum, sName = sLine.split(None, 1)
            try:
                iNum = int(sNum)
            except ValueError:
                raise IOError('Illegal number %s for Lackey CCG deck' % sNum)

            if sName in self._dNameCache:
                sName = self._dNameCache[sName]
        elif sLine != 'Crypt:':
            raise IOError('Illegal string %s for Lackey CCG deck' % sLine)
        else:
            return
        oHolder.add(iNum, sName, None, None)
        return