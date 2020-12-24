# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteSLDeck.py
# Compiled at: 2019-12-11 16:37:58
"""Writer for the Secret Library 'import a deck' web form.

   Example:

   Deck Name: My Deck
   Author: Someone

   Crypt
   ----
   1 Vampire 1
   2 Vampire 2

   Library
   ----
   1 Lib Name
   2 Lib2, The
   """
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.base.Utility import move_articles_to_back
from sutekh.SutekhUtility import is_crypt_card
SL_FIXES = {'Carlton Van Wyk': 'Carlton Van Wyk (Hunter)', 
   'Jake Washington': 'Jake Washington (Hunter)', 
   'Pentex™ Loves You!': 'Pentex(TM) Loves You!', 
   'Pentex™ Subversion': 'Pentex(TM) Subversion', 
   'Nephandus': 'Nephandus (Mage)', 
   'Shadow Court Satyr': 'Shadow Court Satyr (Changeling)', 
   'Amam the Devourer': 'Amam the Devourer (Bane Mummy)', 
   'Wendell Delburton': 'Wendell Delburton (Hunter)', 
   'Dauntain Black Magician': 'Dauntain Black Magician (Changeling)', 
   "Bang Nakh — Tiger's Claws": "Bang Nakh -- Tiger's Claws", 
   'Neighborhood Watch Commander': 'Neighborhood Watch Commander (Hunter)', 
   'Mylan Horseed': 'Mylan Horseed (Goblin)', 
   'Sacré-Cœur Cathedral, France': 'Sacre Cour Cathedral, France', 
   'Ambrosius, The Ferryman': 'Ambrosius, The Ferryman (Wraith)', 
   'Céleste Lamontagne': 'Célèste Lamontagne', 
   "L'Épuisette": "L'Epuisette", 
   'Puppeteer': 'Puppeteer (Wraith)', 
   'Sébastien Goulet': 'Sébastian Goulet', 
   'Sébastien Goulet (Adv)': 'Sébastian Goulet (Adv)', 
   'Akhenaten, The Sun Pharaoh': 'Akhenaten, The Sun Pharaoh (Mummy)', 
   'Tutu the Doubly Evil One': 'Tutu the Doubly Evil One (Bane Mummy)', 
   'Veneficti': 'Veneficti (Mage)', 
   'Brigitte Gebauer': 'Brigitte Gebauer (Wraith)', 
   'Étienne Fauberge': 'Etienne Fauberge', 
   'Kherebutu': 'Kherebutu (Bane Mummy)', 
   'Qetu the Evil Doer': 'Qetu the Evil Doer (Bane Mummy)', 
   'Saatet-ta': 'Saatet-ta (Bane Mummy)', 
   'Mehemet of the Ahl-i-Batin': 'Mehemet of the Ahl-i-Batin (Mage)', 
   'Draeven Softfoot': 'Draeven Softfoot (Changeling)', 
   'Felix Fix Hessian': 'Felix Fix Hessian (Wraith)', 
   'Thadius Zho': 'Thadius Zho, Mage'}

class WriteSLDeck(object):
    """Create a string in SL import format representing a card set."""

    def _escape(self, sName):
        """Escape the card name to SL's requirements"""
        if sName in SL_FIXES:
            sName = SL_FIXES[sName]
        sName = move_articles_to_back(sName)
        sName = sName.replace('(Advanced)', '(Adv)')
        sName = sName.replace('"', '')
        return sName

    def _gen_header(self, oHolder):
        """Add the header"""
        return 'Deck Name: %s\nAuthor: %s\nDescription:\n%s\n' % (
         oHolder.name,
         oHolder.author,
         oHolder.comment)

    def _gen_card_list(self, dCards):
        """Return a list, sorted by name, with the numbers."""
        aResult = []
        for sName in sorted(dCards):
            aResult.append('%d %s\n' % (dCards[sName], sName))

        return ('').join(aResult)

    def _gen_sl_deck(self, oHolder):
        """Process the card set, creating the lines as needed"""
        sResult = self._gen_header(oHolder)
        dCards = {'Crypt': {}, 'Library': {}}
        for oCard in oHolder.cards:
            oAbsCard = IAbstractCard(oCard)
            if is_crypt_card(oAbsCard):
                sType = 'Crypt'
            else:
                sType = 'Library'
            sName = self._escape(oAbsCard.name)
            dCards[sType].setdefault(sName, 0)
            dCards[sType][sName] += 1

        sResult += 'Crypt\n---\n'
        sResult += self._gen_card_list(dCards['Crypt'])
        sResult += '\nLibrary\n---\n'
        sResult += self._gen_card_list(dCards['Library'])
        return sResult

    def write(self, fOut, oHolder):
        """Takes file object + card set to write, and writes an JOL deck
           representing the deck"""
        fOut.write(self._gen_sl_deck(oHolder))