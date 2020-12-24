# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/ArdbInfo.py
# Compiled at: 2019-12-11 16:37:56
"""Base class for the ARDB writers.

   Provide methods for extracting the relevant cards from the card set
   and such.
   """
from sutekh.base.core.BaseAdapters import IAbstractCard, IPhysicalCard
from sutekh.SutekhInfo import SutekhInfo
from sutekh.SutekhUtility import is_crypt_card, is_trifle

def escape_ardb_expansion_name(oExpansion):
    """Rework the expansion name to match ARDB"""
    sExpName = oExpansion.shortname
    if sExpName == 'Promo':
        sExpName = oExpansion.name
        sExpName = sExpName.replace('-', '')
    elif sExpName == 'BSC':
        sExpName = 'CE'
    return sExpName


def unescape_ardb_expansion_name(sExpName):
    """Rework ARBD Promo to Sutekh Promo-"""
    if sExpName.startswith('Promo') and not sExpName.startswith('Promo-'):
        sExpName = sExpName.replace('Promo', 'Promo-')
    return sExpName


class ArdbInfo(object):
    """Create a string in ARDB's text format representing a dictionary
       of cards."""
    sDatabaseVersion = 'Sutekh-20090410'
    sVersionString = SutekhInfo.VERSION_STR
    sFormatVersion = '-TODO-1.0'

    def _get_cards(self, oCardIter):
        """Create the dictionary of cards given the list of cards"""
        dDict = {}
        for oCard in oCardIter:
            oPhysCard = IPhysicalCard(oCard)
            oAbsCard = IAbstractCard(oCard)
            sSet = self._get_ardb_exp_name(oPhysCard)
            dDict.setdefault((oAbsCard, sSet), 0)
            dDict[(oAbsCard, sSet)] += 1

        return dDict

    def _group_sets(self, dCards):
        """Group the cards together regardless of set.

           ARDB inventory doesn't seperate cards by set, although it's included
           in the XML file, so we need to combine things so there's only 1
           entry per card."""
        dCombinedCards = {}
        for tKey, iNum in sorted(dCards.iteritems(), key=lambda x: (
         x[0][0].name, x[0][(-1)])):
            oCard = tKey[0]
            dCombinedCards.setdefault(oCard, [0] + list(tKey[1:]))
            dCombinedCards[oCard][0] += iNum

        return dCombinedCards

    def _group_types(self, dCombinedLib):
        """Group the cards together by card type."""
        dTypes = {}
        for oCard, (iCount, sTypeString, _sSet) in dCombinedLib.iteritems():
            if sTypeString not in dTypes:
                dTypes[sTypeString] = {}
            dTypes[sTypeString].setdefault(oCard, 0)
            dTypes[sTypeString][oCard] += iCount

        return dTypes

    def _count_trifles(self, dCards):
        """Given the result of _extract_library, count the trifles."""
        iCount = 0
        for tKey, iNum in dCards.iteritems():
            oCard = tKey[0]
            if is_trifle(oCard):
                iCount += iNum

        return iCount

    def _extract_crypt(self, dCards):
        """Extract the crypt cards from the list."""
        dCryptStats = {'size': 0, 
           'min': 0, 
           'minsum': 0, 
           'max': 0, 
           'maxsum': 0, 
           'avg': 0.0}
        dVamps = {}
        aCaps = []
        for tKey, iCount in dCards.iteritems():
            oCard = tKey[0]
            if is_crypt_card(oCard):
                dVamps[tKey] = iCount
                dCryptStats['size'] += iCount
                if oCard.cardtype[0].name == 'Vampire':
                    iCap = oCard.capacity
                elif oCard.cardtype[0].name == 'Imbued':
                    iCap = oCard.life
                dCryptStats['avg'] += iCap * iCount
                aCaps.extend([iCap] * iCount)

        if dCryptStats['size'] > 0:
            aCaps.sort()
            dCryptStats['min'] = min(aCaps)
            dCryptStats['max'] = max(aCaps)
            dCryptStats['minsum'] = sum(aCaps[:4])
            dCryptStats['maxsum'] = sum(aCaps[-4:])
            dCryptStats['avg'] = round(dCryptStats['avg'] / dCryptStats['size'], 2)
        return (
         dVamps, dCryptStats)

    def _extract_library(self, dCards):
        """Extract the library cards from the list."""
        iSize = 0
        dLib = {}
        for tKey, iCount in dCards.iteritems():
            oCard, sSet = tKey
            if not is_crypt_card(oCard):
                aTypes = sorted([ x.name for x in oCard.cardtype ])
                sTypeString = ('/').join(aTypes)
                dLib[(oCard, sTypeString, sSet)] = iCount
                iSize += iCount

        return (
         dLib, iSize)

    def _gen_disciplines(self, oCard):
        """Extract the discipline string from the card."""
        if oCard.discipline:
            aDisc = []
            for oDisc in oCard.discipline:
                if oDisc.level == 'superior':
                    aDisc.append(oDisc.discipline.name.upper())
                else:
                    aDisc.append(oDisc.discipline.name)

            aDisc.sort()
            return (' ').join(aDisc)
        if oCard.virtue:
            return (' ').join(sorted([ x.name for x in oCard.virtue ]))
        return ''

    def _format_crypt_line(self, oCard, iCount):
        """Create a dictionary with the basic elements of a crypt card line,
           handling clan, capacity and advanced status consistently."""
        dLine = {'count': iCount}
        if oCard.creed:
            dLine['clan'] = '%s (Imbued)' % [ x.name for x in oCard.creed ][0]
            dLine['capacity'] = oCard.life
        else:
            dLine['clan'] = [ x.name for x in oCard.clan ][0]
            dLine['capacity'] = oCard.capacity
        dLine['name'] = oCard.name
        dLine['adv'] = '   '
        if oCard.level is not None:
            dLine['name'] = dLine['name'].replace(' (Advanced)', '')
            dLine['adv'] = 'Adv'
        dLine['title'] = '   '
        if oCard.title:
            dLine['title'] = [ oC.name for oC in oCard.title ][0]
            dLine['title'] = dLine['title'].replace('Independent with ', '')[:12]
        dLine['group'] = int(oCard.group)
        return dLine

    def _get_cap_key(self, oCard):
        """Get a capacity or life value for the card, with sensible
           defaults for None.

           Intended to avoid "can't compare unequal types" issues"""
        if oCard.capacity:
            return -oCard.capacity
        if oCard.life:
            return -oCard.life
        return 1

    def _crypt_sort_key(self, tItem):
        """Sort the vampire dictionary in ARDB's ordering.

           We sort inversely by count, then capacity,
           then normally by card name."""
        return (
         -tItem[1][0], self._get_cap_key(tItem[0]), tItem[0].name)

    def _get_ardb_exp_name(self, oPhysCard):
        """Extract the correct ARDB name for the expansion"""
        if oPhysCard.printing:
            oExpansion = oPhysCard.printing.expansion
        else:
            oAbsCard = IAbstractCard(oPhysCard)
            aExp = sorted([ oP.expansion for oP in oAbsCard.rarity ], key=lambda x: x.shortname)
            oExpansion = aExp[0]
        sSet = escape_ardb_expansion_name(oExpansion)
        return sSet