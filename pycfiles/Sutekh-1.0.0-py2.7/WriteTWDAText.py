# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteTWDAText.py
# Compiled at: 2019-12-11 16:37:57
"""Writer for the text format preferred for TWDA entries.

   Example deck:

   Deck Name: Modified Followers of Set Preconstructed Deck
   Author: An Author
   Description:
   Followers of Set Preconstructed Starter from Lords of the Night.

   http://www.white-wolf.com/vtes/index.php?line=Checklist_LordsOfTheNight

   Crypt (12 cards, min=10 max=40 avg=5.84)
   ----------------------------------------
   2x Nakhthorheb       10 OBF PRE SER                        Follower of Set:4
   2x Renenet       5 OBF PRE ser                         Follower of Set:4
   1x Neferu        9 OBF PRE SER THA dom nec   2 votes   Follower of Set:4
   1x Arcadian, The 8 DOM MYT OBT chi for                 Kiasyd:5
   ...

   Library (77 cards)
   Master (4; 1 trifle)
     2x Barrens, The
     1x Sudden Reversal
     1x Wash

   Action (20)
     2x Blithe Acceptance
     4x Dream World

   Ally (1)
     1x Carlton Van Wyk

   Equipment (2)
     2x .44 Magnum

   Political Action (1)
     1x Parity Shity

   Action Modifier (3)
   ...
   """
from sutekh.base.Utility import move_articles_to_back
from sutekh.core.ArdbInfo import ArdbInfo
SPECIAL_NAMES = {'Pentex™ Loves You!': 'Pentex(TM) Loves You!', 
   'Pentex™ Subversion': 'Pentex(TM) Subversion'}
SECTION_ORDER = ('Master', 'Conviction', 'Action', 'Ally', 'Equipment', 'Political Action',
                 'Power', 'Retainer', 'Action Modifier', 'Reaction', 'Combat', 'Event')

def format_avg(fAvg):
    """The TWDA doesn't want trailing zeros in the average, so we
       strip those here"""
    iIntPart = int(fAvg)
    fFracPart = fAvg - iIntPart
    sResult = '%d' % iIntPart
    if fFracPart > 0.001:
        sFrac = '%.2g' % fFracPart
        sResult += sFrac[1:]
    return sResult


def normalise_card_name(sName):
    """Normalise the name as needed for the TWDA"""
    sName = move_articles_to_back(sName)
    return SPECIAL_NAMES.get(sName, sName)


class WriteTWDAText(ArdbInfo):
    """Create a string in ARDB's text format representing a dictionary
       of cards."""

    def _gen_header(self, oHolder):
        """Generate an TWDA text file header."""
        return 'Deck Name: %s\nAuthor: %s\nDescription:\n%s\n' % (
         oHolder.name, oHolder.author,
         oHolder.comment)

    def _crypt_sort_key(self, tItem):
        """Sort the crypt cards.

           We override the base class so we can sort by the modified name."""
        return (
         -tItem[1][0], self._get_cap_key(tItem[0]),
         move_articles_to_back(tItem[0].name).lower())

    def _gen_crypt(self, dCards):
        """Generate an TWDA text file crypt description.

           dCards is mapping of (card id, card name) -> card count.
           """
        dVamps, dCryptStats = self._extract_crypt(dCards)
        dCryptStats['formatted_avg'] = format_avg(dCryptStats['avg'])
        dCombinedVamps = self._group_sets(dVamps)
        sCryptLine = 'Crypt (%(size)d cards, min=%(minsum)d, max=%(maxsum)d, avg=%(formatted_avg)s)' % dCryptStats
        sCrypt = sCryptLine + '\n' + '-' * len(sCryptLine) + '\n'
        aCryptLines = []
        iCountSpace = 3
        iNameJust = 8
        iDiscJust = 0
        iTitleJust = 0
        for oCard, (iCount, _sSet) in sorted(dCombinedVamps.iteritems(), key=self._crypt_sort_key):
            dLine = self._format_crypt_line(oCard, iCount)
            if 'Imbued' in dLine['clan']:
                dLine['clan'].replace(' (Imbued)', '')
            dLine['disc'] = self._gen_disciplines(oCard)
            if not dLine['disc']:
                dLine['disc'] = '-none-'
            dLine['name'] = normalise_card_name(dLine['name'])
            iNameJust = max(iNameJust, len(dLine['name']))
            iDiscJust = max(iDiscJust, len(dLine['disc']))
            if iCount > 10:
                iCountSpace = 4
            dLine['title'] = dLine['title'].strip()
            iTitleJust = max(iTitleJust, len(dLine['title']))
            aCryptLines.append(dLine)
            if dLine['adv'] == 'Adv':
                dLine['name'] += ' (ADV)'

        iCapacityPos = iCountSpace + iNameJust + 1
        if iCapacityPos < 24:
            iCapacityPos = 24
        iNameJust = iCapacityPos // 8 * 8
        iDiscJust = (iCapacityPos + 2 + iDiscJust) // 8 * 8
        if iTitleJust:
            iTitleJust = (iDiscJust + 16) // 8 * 8
        for dLine in aCryptLines:
            if iCountSpace == 3:
                sCount = '%(count)dx ' % dLine
            else:
                sCount = '%(count)2dx ' % dLine
            iPos = iCountSpace + len(dLine['name'])
            while iPos < iNameJust:
                dLine['name'] += '\t'
                iPos = iPos + 8 - (iPos + 8) % 8

            dLine['name'] += ' ' * (iCapacityPos - iPos)
            sDisc = '%(capacity)-3d %(disc)s' % dLine
            iPos = iCapacityPos + len(sDisc)
            iTabPos = iPos - iPos % 8
            sPadd = ''
            while iTabPos <= iDiscJust:
                sPadd += '\t'
                iTabPos += 8
                iPos = iTabPos + 8

            if sPadd == '' and iTabPos > 40:
                sPadd = '\t'
                iPos = iTabPos + 8
            dLine['disc'] = sDisc + sPadd
            if iTitleJust:
                iEndPos = iTitleJust - len(dLine['title']) - iDiscJust + 7
                iPadding = iEndPos // 8
                dLine['title'] = dLine['title'].lower() + '\t' * iPadding
            sCrypt += sCount + '%(name)s%(disc)s%(title)s%(clan)s:%(group)d\n' % dLine
            if sCrypt.endswith(':-1\n'):
                sCrypt = sCrypt.replace(':-1', ':ANY')

        return sCrypt

    def _gen_library(self, dCards):
        """Generaten an TWDA text file library description.

           dCards is mapping of (card id, card name) -> card count.
           """
        dLib, iLibSize = self._extract_library(dCards)
        dCombinedLib = self._group_sets(dLib)
        dTypes = self._group_types(dCombinedLib)
        sLib = 'Library (%d cards)\n' % (
         iLibSize,)
        aSortedTypes = sorted(dTypes)
        aProcessed = set()
        for sTypeString in SECTION_ORDER:
            dCards = {}
            for sCandidate in aSortedTypes:
                if sCandidate in aProcessed:
                    continue
                if sTypeString == sCandidate:
                    dCards = dTypes[sCandidate]
                    aProcessed.add(sCandidate)
                else:
                    if sCandidate.startswith(sTypeString + '/'):
                        dCards = dTypes[sCandidate]
                        aProcessed.add(sCandidate)
                    else:
                        continue
                    iTotal = sum(dCards.values())
                    if sTypeString == 'Master':
                        iTrifles = self._count_trifles(dLib)
                        if iTrifles:
                            sLib += '%s (%d; %d trifle)\n' % (sTypeString,
                             iTotal, iTrifles)
                        else:
                            sLib += '%s (%d)\n' % (sCandidate, iTotal)
                    else:
                        sLib += '\n'
                        sLib += '%s (%d)\n' % (sCandidate, iTotal)
                    fKey = lambda x: move_articles_to_back(x[0].name).lower()
                    for oCard, iCount in sorted(dCards.iteritems(), key=fKey):
                        sName = normalise_card_name(oCard.name)
                        sLib += '%dx %s\n' % (iCount, sName)

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