# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/CardSetHolder.py
# Compiled at: 2019-12-11 16:37:48
"""Holder for card set (Abstract or Physical) data before it is committed
   to a database."""
from sqlobject import SQLObjectNotFound, sqlhub
from .CardLookup import DEFAULT_LOOKUP
from .BaseTables import PhysicalCardSet

class CardSetHolder(object):
    """Holder for Card Sets.

       This holds a list of cards and optionally expansions and may be used
       to create a PhysicalCardSet. We call on the provided CardLookup function
       to resolve unknown cards.
       """

    def __init__(self):
        self._sName, self._sAuthor, self._sComment, self._sAnnotations = (None, '',
                                                                          '', '')
        self._bInUse = False
        self._sParent = None
        self._dCards = {}
        self._dExpansions = {}
        self._aWarnings = []
        self._dCardExpansions = {}
        return

    def add(self, iCnt, sName, sExpansionName, sPrintingName):
        """Append cards to the virtual set.

           sExpansionName may be None.
           """
        self._dCards.setdefault(sName, 0)
        self._dCards[sName] += iCnt
        tExp = (sExpansionName, sPrintingName)
        self._dExpansions.setdefault(tExp, 0)
        self._dExpansions[tExp] += iCnt
        self._dCardExpansions.setdefault(sName, {})
        self._dCardExpansions[sName].setdefault(tExp, 0)
        self._dCardExpansions[sName][tExp] += iCnt

    def remove(self, iCnt, sName, sExpansionName, sPrintingName):
        """Remove cards from the virtual set.

           sExpansionName may be None.
           """
        tExp = (
         sExpansionName, sPrintingName)
        if sName not in self._dCards or self._dCards[sName] < iCnt:
            raise RuntimeError("Not enough of card '%s' to remove '%d'." % (
             sName, iCnt))
        elif sName not in self._dCardExpansions or tExp not in self._dCardExpansions[sName] or self._dCardExpansions[sName][tExp] < iCnt:
            raise RuntimeError("Not enough of card '%s' from expansion '%s (%s)' to remove '%d'." % (
             sName,
             sExpansionName,
             sPrintingName,
             iCnt))
        self._dCardExpansions[sName][tExp] -= iCnt
        self._dExpansions[tExp] -= iCnt
        self._dCards[sName] -= iCnt

    def _set_name(self, sValue):
        """Set the name, ensuring we have santised any encoding issues"""
        self._sName = self._sanitise_text(sValue, 'the card set name', True)

    name = property(fget=lambda self: self._sName, fset=_set_name)
    author = property(fget=lambda self: self._sAuthor, fset=lambda self, x: setattr(self, '_sAuthor', x))
    comment = property(fget=lambda self: self._sComment, fset=lambda self, x: setattr(self, '_sComment', x))
    annotations = property(fget=lambda self: self._sAnnotations, fset=lambda self, x: setattr(self, '_sAnnotations', x))
    inuse = property(fget=lambda self: self._bInUse, fset=lambda self, x: setattr(self, '_bInUse', x))
    parent = property(fget=lambda self: self._sParent, fset=lambda self, x: setattr(self, '_sParent', x))
    num_entries = property(fget=lambda self: len(self._dCards))

    def get_parent_pcs(self):
        """Get the parent PCS, or none if no parent exists."""
        if self.parent:
            try:
                oParent = PhysicalCardSet.selectBy(name=self.parent).getOne()
            except SQLObjectNotFound:
                self.add_warning('Parent Card Set %s not found' % self.parent)
                oParent = None

        else:
            oParent = None
        return oParent

    def get_warnings(self):
        """Get any warning messages from the holder"""
        return self._aWarnings

    def add_warning(self, sMsg):
        """Add a warning message to the list of warnings."""
        self._aWarnings.append(sMsg)

    def clear_warnings(self):
        """Reset the warning messages list"""
        self._aWarnings = []

    def create_pcs(self, oCardLookup=DEFAULT_LOOKUP):
        """Create a Physical Card Set.
           """
        if self.name is None:
            raise RuntimeError('No name for the card set')
        aCardCnts = self._dCards.items()
        aAbsCards = oCardLookup.lookup([ tCardCnt[0] for tCardCnt in aCardCnts ], 'Card Set "%s"' % self.name)
        dNameCards = dict(zip(self._dCards, aAbsCards))
        dPrintingLookup = oCardLookup.printing_lookup(self._dExpansions, 'Physical Card List', self._dCardExpansions)
        aPhysCards = oCardLookup.physical_lookup(self._dCardExpansions, dNameCards, dPrintingLookup, 'Card Set "%s"' % self.name)
        if hasattr(sqlhub.processConnection, 'commit'):
            self._commit_pcs(aPhysCards)
        else:
            sqlhub.doInTransaction(self._commit_pcs, aPhysCards)
        return

    def _sanitise_text(self, sText, sIdentifier, bIncludeFallback):
        """Helper function to handle wierd encodings in the input
           sanely.

           bIncludeFallback controls how any encoding errors are logged."""
        try:
            if sText:
                sSane = sText.encode('utf8')
            else:
                sSane = sText
        except UnicodeDecodeError:
            sSane = sText.decode('ascii', 'replace').encode('ascii', 'replace')
            if bIncludeFallback:
                self.add_warning('Unexpected encoding encountered for %s.\nReplaced with %s.' % (
                 sIdentifier, sSane))
            else:
                self.add_warning('Unexpected encoding encountered for %s.\nUsed Ascii fallback.' % sIdentifier)

        return sSane

    def _commit_pcs(self, aPhysCards):
        """Commit the card set to the database."""
        oParent = self.get_parent_pcs()
        oPCS = PhysicalCardSet(name=self.name, author=self._sanitise_text(self.author, 'the card set author', True), comment=self._sanitise_text(self.comment, 'the comments', False), annotations=self._sanitise_text(self.annotations, 'the annotations', False), inuse=self.inuse, parent=oParent)
        oPCS.syncUpdate()
        for oPhysCard in aPhysCards:
            if not oPhysCard:
                continue
            oPCS.addPhysicalCard(oPhysCard.id)

        oPCS.syncUpdate()


class CardSetWrapper(CardSetHolder):
    """CardSetHolder class which provides a read-only wrapper of a card set."""

    def __init__(self, oCS):
        self._oCS = oCS
        self._aWarnings = []

    def add(self, iCnt, sName, sExpansionName, sPrintingName):
        """Not allowed to append cards."""
        raise NotImplementedError('CardSetWrapper is read-only')

    def remove(self, iCnt, sName, sExpansionName, sPrintingName):
        """Not allowed to remove cards."""
        raise NotImplementedError('CardSetWrapper is read-only')

    def create_pcs(self, oCardLookup=DEFAULT_LOOKUP):
        """Can't create a Physical Card Set -- there is one already."""
        raise NotImplementedError('CardSetWrapper is read-only')

    def _get_cs_attr(self, sAttr):
        """Get attribute, returning '' if unset"""
        sValue = getattr(self._oCS, sAttr)
        if sValue:
            return sValue
        return ''

    def _parent_name(self):
        """Return the parent card set's name or None if their is no parent."""
        if self._oCS.parent is None:
            return
        else:
            return self._oCS.parent.name

    name = property(fget=lambda self: self._get_cs_attr('name'))
    author = property(fget=lambda self: self._get_cs_attr('author'))
    comment = property(fget=lambda self: self._get_cs_attr('comment'))
    annotations = property(fget=lambda self: self._get_cs_attr('annotations'))
    inuse = property(fget=lambda self: self._oCS.inuse)
    parent = property(fget=lambda self: self._parent_name())
    num_entries = property(fget=lambda self: len(self._oCS.cards))
    cards = property(fget=lambda self: self._oCS.cards)

    def get_parent_pcs(self):
        """Get the parent PCS, or none if no parent exists."""
        return self._oCS.parent


class CachedCardSetHolder(CardSetHolder):
    """CardSetHolder class which supports creating and using a
       cached dictionary of Lookup results.
       """

    def create_pcs(self, oCardLookup=DEFAULT_LOOKUP, dLookupCache={}):
        """Create a Physical Card Set.

           dLookupCache is updated as soon as possible, i.e. immediately after
           calling oCardLookup.lookup(...).
           """
        dLookupCache.setdefault('cards', {})
        dLookupCache.setdefault('printings', {})
        if self.name is None:
            raise RuntimeError('No name for the card set')
        aCardCnts = self._dCards.items()
        aAbsCards = oCardLookup.lookup([ dLookupCache['cards'].get(tCardCnt[0], tCardCnt[0]) for tCardCnt in aCardCnts
                                       ], 'Card Set "%s"' % self.name)
        dNameCards = dict(zip(self._dCards, aAbsCards))
        for oAbs, (sName, _iCnt) in zip(aAbsCards, aCardCnts):
            if not oAbs:
                dLookupCache['cards'][sName] = None
            else:
                dLookupCache['cards'][sName] = oAbs.canonicalName

        aExpPrintNames = []
        for tExpPrint in self._dExpansions:
            tNewExpPrint = dLookupCache['printings'].get(tExpPrint, tExpPrint)
            aExpPrintNames.append(tNewExpPrint)

        dCardExpansions = {}
        for sName in self._dCardExpansions:
            dCardExpansions[sName] = {}
            for tExpPrint, iCnt in self._dCardExpansions[sName].iteritems():
                tNewExpPrint = dLookupCache['printings'].get(tExpPrint, tExpPrint)
                dCardExpansions[sName][tNewExpPrint] = iCnt

        dPrintingLookup = oCardLookup.printing_lookup(aExpPrintNames, 'Physical Card List', dCardExpansions)
        for tExpPrint, oPrinting in dPrintingLookup.iteritems():
            if not oPrinting:
                dLookupCache['printings'][tExpPrint] = (None, None)
            else:
                dLookupCache['printings'][tExpPrint] = (
                 oPrinting.expansion.name, oPrinting.name)

        aPhysCards = oCardLookup.physical_lookup(dCardExpansions, dNameCards, dPrintingLookup, 'Card Set "%s"' % self.name)
        if hasattr(sqlhub.processConnection, 'commit'):
            self._commit_pcs(aPhysCards)
        else:
            sqlhub.doInTransaction(self._commit_pcs, aPhysCards)
        return


def make_card_set_holder(oCardSet):
    """Given a CardSet, create a Cached Card Set Holder for it."""
    oCS = CachedCardSetHolder()
    oCS.name = oCardSet.name
    oCS.author = oCardSet.author
    oCS.comment = oCardSet.comment
    oCS.annotations = oCardSet.annotations
    oCS.inuse = oCardSet.inuse
    if oCardSet.parent:
        oCS.parent = oCardSet.parent.name
    for oCard in oCardSet.cards:
        if oCard.printing is None:
            oCS.add(1, oCard.abstractCard.canonicalName, None, None)
        else:
            oCS.add(1, oCard.abstractCard.canonicalName, oCard.printing.expansion.name, oCard.printing.name)

    return oCS