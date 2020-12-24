# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteJOL.py
# Compiled at: 2019-12-11 16:37:58
"""Writer for the JOL format.

   We use the "Num"x"Name" format for created decks, as being shorter

   Example:

   4xVampire 1
   Vampire 2
   2xVampire 3

   2xLib Name

   """
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.core.ELDBUtilities import type_of_card

class WriteJOL(object):
    """Create a string in JOL format representing a card set."""

    def _escape(self, sName):
        """Escape the card name to JOL's requirements"""
        sName = sName.replace('(Advanced)', '(advanced)')
        return sName

    def _gen_inv(self, oHolder):
        """Process the card set, creating the lines as needed"""
        dCards = {'Crypt': {}, 'Library': {}}
        sResult = ''
        for oCard in oHolder.cards:
            oAbsCard = IAbstractCard(oCard)
            sType = type_of_card(oAbsCard)
            sName = self._escape(oAbsCard.name)
            dCards[sType].setdefault(sName, 0)
            dCards[sType][sName] += 1

        for sType in dCards:
            for sName, iNum in sorted(dCards[sType].items()):
                if iNum > 1:
                    sResult += '%dx%s\n' % (iNum, sName)
                else:
                    sResult += '%s\n' % sName

            if sType == 'Crypt':
                sResult += '\n'

        return sResult

    def write(self, fOut, oHolder):
        """Takes file object + card set to write, and writes an JOL deck
           representing the deck"""
        fOut.write(self._gen_inv(oHolder))