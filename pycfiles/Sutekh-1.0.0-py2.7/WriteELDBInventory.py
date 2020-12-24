# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteELDBInventory.py
# Compiled at: 2019-12-11 16:37:58
"""Writer for the FELDB inventory format.

   Example:

   "ELDB - Inventory"
   "Aabbt Kindred",1,0,"","Crypt"
   "Aaron Duggan, Cameron`s Toady",0,0,"","Crypt"
   ...
   "Zip Line",0,0,"","Library"
   """
from sutekh.base.core.BaseTables import AbstractCard
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.core.ELDBUtilities import norm_name, type_of_card

class WriteELDBInventory(object):
    """Create a string in ELDB inventory format representing a card set."""

    def _gen_header(self):
        """Generate an ELDB inventory file header."""
        return '"ELDB - Inventory"'

    def _gen_inv(self, oHolder):
        """Process the card set, creating the lines as needed"""
        dCards = {}
        sResult = ''
        for oCard in AbstractCard.select():
            dCards[oCard] = 0

        for oCard in oHolder.cards:
            oAbsCard = IAbstractCard(oCard)
            dCards[oAbsCard] += 1

        for oCard, iNum in dCards.iteritems():
            sResult += '"%s",%d,0,"","%s"\n' % (norm_name(oCard), iNum,
             type_of_card(oCard))

        return sResult

    def write(self, fOut, oHolder):
        """Takes file object + card set to write, and writes an ELDB inventory
           representing the deck"""
        fOut.write(self._gen_header())
        fOut.write('\n')
        fOut.write(self._gen_inv(oHolder))