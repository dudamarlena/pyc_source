# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteLackeyCCG.py
# Compiled at: 2019-12-11 16:37:58
"""Writer for the Lackey CCG file format.
     (AFAICT, the tabs aren't required, but Lackey uses them, so I'm playing
      safe)

   Example:

   2    Card 1
   3    Card 2
   1    Card 3
   Crypt:
   1    Vampire 1
   2    Vampire 2

   """
import unicodedata
from sutekh.core.ELDBUtilities import type_of_card
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.base.Utility import move_articles_to_back

def lackey_name(oCard):
    """Escape the card name to Lackey CCG's requirements"""
    sName = oCard.name
    if oCard.level is not None:
        sName = sName.replace('(Advanced)', 'Adv.')
    sName = move_articles_to_back(sName)
    if oCard.cardtype[0].name == 'Imbued':
        sName = sName.replace('"', "''")
    else:
        sName = sName.replace('"', "'")
    sName = unicodedata.normalize('NFKD', sName).encode('ascii', 'ignore')
    return sName


class WriteLackeyCCG(object):
    """Create a string in Lackey CCG format representing a card set."""

    def _gen_inv(self, oHolder):
        """Process the card set, creating the lines as needed"""
        dCards = {'Crypt': {}, 'Library': {}}
        sResult = ''
        for oCard in oHolder.cards:
            sType = type_of_card(IAbstractCard(oCard))
            sName = lackey_name(IAbstractCard(oCard))
            dCards[sType].setdefault(sName, 0)
            dCards[sType][sName] += 1

        for sType in ['Library', 'Crypt']:
            for sName, iNum in sorted(dCards[sType].items()):
                sResult += '%d\t%s\n' % (iNum, sName)

            if sType == 'Library':
                sResult += 'Crypt:\n'

        return sResult

    def write(self, fOut, oHolder):
        """Takes file object + card set to write, and writes an Lackey CCG
           deck representing the card set"""
        fOut.write(self._gen_inv(oHolder))