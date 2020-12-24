# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/BaseGroupings.py
# Compiled at: 2019-12-11 16:37:48
"""Provide classes to change the way cards are grouped in the display"""

class IterGrouping(object):
    """Bass class for the groupings"""

    def __init__(self, oIter, fKeys):
        """Create the grouping

           oIter: Iterable to group.
           fKeys: Function which maps an item from the iterable
                  to a list of keys. Keys must be hashable.
           """
        self.__oIter = oIter
        self.__fKeys = fKeys

    def __iter__(self):
        dKeyItem = {}
        for oItem in self.__oIter:
            aSet = set(self.__fKeys(oItem))
            if aSet:
                for oKey in aSet:
                    dKeyItem.setdefault(oKey, []).append(oItem)

            else:
                dKeyItem.setdefault(None, []).append(oItem)

        aList = dKeyItem.keys()
        aList.sort()
        for oKey in aList:
            yield (oKey, dKeyItem[oKey])

        return


DEF_GET_CARD = lambda x: x

class CardTypeGrouping(IterGrouping):
    """Group by card type. This is the default grouping. This grouping
       places cards with multiple types in each group to which it belongs."""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):
        super(CardTypeGrouping, self).__init__(oIter, lambda x: [ y.name for y in fGetCard(x).cardtype ])


class MultiTypeGrouping(IterGrouping):
    """Group by card type, but make separate groupings for
       cards which have multiple types."""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):

        def multitype(x):
            """Return a list of one string with slash separated card types."""
            aTypes = [ y.name for y in fGetCard(x).cardtype ]
            aTypes.sort()
            return [(' / ').join(aTypes)]

        super(MultiTypeGrouping, self).__init__(oIter, multitype)


class ExpansionGrouping(IterGrouping):
    """Group by the expansions in which the cards have been printed."""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):
        super(ExpansionGrouping, self).__init__(oIter, lambda x: [ y.expansion.name for y in fGetCard(x).rarity
        ])


class RarityGrouping(IterGrouping):
    """ Group the cards by the published rarity."""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):
        super(RarityGrouping, self).__init__(oIter, lambda x: [ y.rarity.name for y in fGetCard(x).rarity
        ])


class BaseExpansionRarityGrouping(IterGrouping):
    """Groups cards by both expansion and rarity."""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):

        def expansion_rarity(oCard):
            aExpRarities = []
            aRarities = list(fGetCard(oCard).rarity)
            for oRarity in aRarities:
                if oRarity.expansion.name.startswith('Promo'):
                    aExpRarities.append('Promo')
                else:
                    aExpRarities.append('%s : %s' % (oRarity.expansion.name,
                     oRarity.rarity.name))
                self._handle_extra_expansions(oRarity, aRarities, aExpRarities)

            return aExpRarities

        super(BaseExpansionRarityGrouping, self).__init__(oIter, expansion_rarity)

    def _handle_extra_expansions(self, oRarity, aRarities, aExpRarities):
        pass


class ArtistGrouping(IterGrouping):
    """Group by Artist"""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):
        super(ArtistGrouping, self).__init__(oIter, lambda x: [ y.name for y in fGetCard(x).artists
        ])


class KeywordGrouping(IterGrouping):
    """Group by Keyword"""

    def __init__(self, oIter, fGetCard=DEF_GET_CARD):
        super(KeywordGrouping, self).__init__(oIter, lambda x: [ y.keyword for y in fGetCard(x).keywords ])


class NullGrouping(IterGrouping):
    """Group everything into a single group named 'All'."""

    def __init__(self, oIter, _fGetCard=DEF_GET_CARD):
        super(NullGrouping, self).__init__(oIter, lambda x: ['All'])