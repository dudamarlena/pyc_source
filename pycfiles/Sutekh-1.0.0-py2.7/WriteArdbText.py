# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteArdbText.py
# Compiled at: 2019-12-11 16:37:58
"""Writer for ther ARDB text deck format.

   Example deck:

   Deck Name : Followers of Set Preconstructed Deck
   Author : L. Scott Johnson
   Description :
   Followers of Set Preconstructed Starter from Lords of the Night.

   http://www.white-wolf.com/vtes/index.php?line=Checklist_LordsOfTheNight

   Crypt [12 vampires] Capacity min: 2 max: 10 average: 5.84
   ------------------------------------------------------------
   2x Nakhthorheb                         10 OBF PRE SER           Follower :4
   ...

   Library [77 cards]
   ------------------------------------------------------------
   Action [20]
     2x Blithe Acceptance
     4x Dream World
   ...
   """
from sutekh.core.ArdbInfo import ArdbInfo

class WriteArdbText(ArdbInfo):
    """Create a string in ARDB's text format representing a dictionary
       of cards."""

    def _gen_header(self, oHolder):
        """Generate an ARDB text file header."""
        return 'Deck Name : %s\nAuthor : %s\nDescription :\n%s\n' % (
         oHolder.name, oHolder.author,
         oHolder.comment)

    def _gen_crypt(self, dCards):
        """Generaten an ARDB text file crypt description.

           dCards is mapping of (card id, card name) -> card count.
           """
        dVamps, dCryptStats = self._extract_crypt(dCards)
        dCombinedVamps = self._group_sets(dVamps)
        sCrypt = 'Crypt [%(size)d vampires] Capacity min: %(min)d max: %(max)d average: %(avg).2f\n------------------------------------------------------------\n' % dCryptStats
        aCryptLines = []
        iDiscJust = 0
        iTitleJust = 0
        for oCard, (iCount, _sSet) in sorted(dCombinedVamps.iteritems(), key=self._crypt_sort_key):
            dLine = self._format_crypt_line(oCard, iCount)
            if dLine['clan'].endswith('antitribu'):
                dLine['clan'] = '!' + dLine['clan'].replace(' antitribu', '')
            elif 'Imbued' not in dLine['clan']:
                dLine['clan'] = dLine['clan'][:10]
            dLine['name'] = dLine['name'].ljust(18)[:18]
            dLine['disc'] = self._gen_disciplines(oCard)
            iDiscJust = max(iDiscJust, len(dLine['disc']))
            iTitleJust = max(iTitleJust, len(dLine['title']))
            aCryptLines.append(dLine)

        for dLine in aCryptLines:
            dLine['title'] = dLine['title'].ljust(iTitleJust)
            dLine['disc'] = dLine['disc'].ljust(iDiscJust)
            sCrypt += ' %(count)dx %(name)s %(adv)s %(capacity)d %(disc)s %(title)s %(clan)s:%(group)d\n' % dLine

        return sCrypt

    def _gen_library(self, dCards):
        """Generaten an ARDB text file library description.

           dCards is mapping of (card id, card name) -> card count.
           """
        dLib, iLibSize = self._extract_library(dCards)
        dCombinedLib = self._group_sets(dLib)
        dTypes = self._group_types(dCombinedLib)
        sLib = 'Library [%d cards]\n------------------------------------------------------------\n' % (
         iLibSize,)
        for sTypeString in sorted(dTypes):
            dCards = dTypes[sTypeString]
            iTotal = sum(dCards.values())
            if sTypeString == 'Master':
                iTrifles = self._count_trifles(dLib)
                if iTrifles > 1:
                    sLib += '%s [%d] (%d trifles)\n' % (sTypeString,
                     iTotal, iTrifles)
                elif iTrifles == 1:
                    sLib += '%s [%d] (%d trifle)\n' % (sTypeString,
                     iTotal, iTrifles)
                else:
                    sLib += '%s [%d]\n' % (sTypeString, iTotal)
            else:
                sLib += '%s [%d]\n' % (sTypeString, iTotal)
            for oCard, iCount in sorted(dCards.iteritems(), key=lambda x: x[0].name):
                sLib += ' %dx %s\n' % (iCount, oCard.name)

            sLib += '\n'

        return sLib

    def write(self, fOut, oHolder):
        """Takes filename, deck details and a dictionary of cards, of the
           form dCard[(id, name, set)] = count and writes the file."""
        dCards = self._get_cards(oHolder.cards)
        fOut.write(self._gen_header(oHolder))
        fOut.write('\n')
        fOut.write(self._gen_crypt(dCards))
        fOut.write('\n')
        fOut.write(self._gen_library(dCards))