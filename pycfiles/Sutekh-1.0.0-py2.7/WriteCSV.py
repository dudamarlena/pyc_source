# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/WriteCSV.py
# Compiled at: 2019-12-11 16:37:52
"""Writer for the CSV format.

   Example (for VtES):

   "Card Name", "Expansion", "Number"
   "Aabbt Kindred","Final Nights", 2
   "Inez ""Nurse216"" Villagrande", "Nights of Reckoning", 1
   "Aire of Elation", "Camarilla Edition", 3
   "Aire of Elation", "Anarchs", 3
   "Zip Line", "Twilight Rebellion", 3
   """

class WriteCSV(object):
    """Create a string in CSV format representing a card set."""

    def __init__(self, bIncludeHeader=True, bIncludeExpansion=True):
        self.bIncludeHeader = bIncludeHeader
        self.bIncludeExpansion = bIncludeExpansion

    def _expansion_name(self, oCard):
        """Utility function to return iether the name, or the appropriate
           placeholder for oExpansion is None."""
        if oCard.printing and self.bIncludeExpansion:
            return oCard.printing.expansion.name
        return 'Unknown Expansion'

    def _gen_header(self):
        """Generate column headers."""
        if self.bIncludeHeader:
            if self.bIncludeExpansion:
                return '"Card Name", "Expansion", "Number"\n'
            return '"Card Name", "Number"\n'
        return ''

    def _gen_inv(self, oHolder):
        """Process the card set, creating the lines as needed"""
        dCards = {}
        sResult = ''
        for oCard in oHolder.cards:
            tKey = (oCard.abstractCard.name.replace('"', '""'),
             self._expansion_name(oCard))
            dCards.setdefault(tKey, 0)
            dCards[tKey] += 1

        for tKey, iNum in sorted(dCards.items(), key=lambda x: x[0]):
            if self.bIncludeExpansion:
                sResult += '"%s", "%s", %d\n' % (tKey[0], tKey[1], iNum)
            else:
                sResult += '"%s", %d\n' % (tKey[0], iNum)

        return sResult

    def write(self, fOut, oHolder):
        """Takes file object + card set to write, and writes an ELDB inventory
           representing the deck"""
        sHeader = self._gen_header()
        if sHeader:
            fOut.write(sHeader)
        fOut.write(self._gen_inv(oHolder))