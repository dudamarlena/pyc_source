# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/CardLookup.py
# Compiled at: 2019-12-11 16:37:48
"""Lookup AbstractCards for a list of card names.
   """
from sqlobject import SQLObjectNotFound
from .BaseAdapters import IPhysicalCard, IExpansion, IAbstractCard, IPrinting

class LookupFailed(Exception):
    """Raised when an AbstractCard lookup fails completed.
       """
    pass


class AbstractCardLookup(object):
    """Base class for objects which translate card names into abstract card
       objects.
       """

    def lookup(self, aNames, sInfo):
        """Return a list of AbstractCards, one for each item in aNames.

           Names for which AbstractCards could not be found will be marked with
           a None in the returned list. The method may raise LookupFailed
           if the entire list should be considered invalid (e.g. if the names
           are presented to a user who then cancels the operation).
           """
        raise NotImplementedError


class PhysicalCardLookup(object):
    """Base class for objects which translate card and expansion names
       into physical card objects
       """

    def physical_lookup(self, dCardExpansions, dNameCards, dNamePrintings, sInfo):
        """Returns a list of physical cards. Since physical cards can't
           be repeated, this is a list of statisfable requests.

           dCardExpansions[Name][Expansion] is the number of cards requested,
           dNameCards is a dictionary of card name to abstract card mappings
           and dNameExps is a dictionary of expansion name to expansion object
           mappings.

           Note that len(list returned) =< sum(all requests in dCardExpansions)

           The physical card list will be smaller if no matching card can be
           found in the physical card list or if dAbstactCards has elements
           that have been excluded.

           LookupFailed will be raised if the entire list should be considered
           invalid, as for AbstractCardLookup
           """
        raise NotImplementedError


class PrintingLookup(object):
    """Base class for objects which translate expansion + print names
       into printing objects
       """

    def printing_lookup(self, aExpPrintNames, sInfo, dCardExpansions):
        """Return a dictionary mapping entries in aExpPrintNames to
           the corresponding print info.

           Names for which printings could not be found will be marked as
           None. This method may raise LookupFailed if the entire list
           should be considered invalid."""
        raise NotImplementedError


class SimpleLookup(AbstractCardLookup, PhysicalCardLookup, PrintingLookup):
    """A really straightforward lookup of AbstractCards and PhysicalCards.

       The default when we don't have a more cunning plan.
       """

    def lookup(self, aNames, _sInfo):
        """A lookup method that excludes unknown cards."""
        aCards = []
        for sName in aNames:
            if sName:
                try:
                    oAbs = IAbstractCard(sName)
                    aCards.append(oAbs)
                except SQLObjectNotFound:
                    aCards.append(None)

            else:
                aCards.append(None)

        return aCards

    def physical_lookup(self, dCardExpansions, dNameCards, dNamePrintings, _sInfo):
        """Lookup cards in the physical card set, excluding unknown cards."""
        aCards = []
        for sName in dCardExpansions:
            oAbs = dNameCards[sName]
            if oAbs is not None:
                for tExpPrint in dCardExpansions[sName]:
                    try:
                        iCnt = dCardExpansions[sName][tExpPrint]
                        oPrinting = dNamePrintings[tExpPrint]
                        aCards.extend([
                         IPhysicalCard((oAbs, oPrinting))] * iCnt)
                    except SQLObjectNotFound:
                        pass

        return aCards

    def printing_lookup(self, aExpPrintNames, _sInfo, _dCardExpansions):
        """Lookup for printing names, excluding unkown expansions or
           printings."""
        dPrintings = {}
        for sExp, sPrintName in aExpPrintNames:
            dPrintings.setdefault((sExp, sPrintName), None)
            oExp = None
            if sExp:
                try:
                    oExp = IExpansion(sExp)
                except SQLObjectNotFound:
                    oExp = None

            if not oExp:
                continue
            try:
                oPrinting = IPrinting((oExp, sPrintName))
            except SQLObjectNotFound:
                oPrinting = IPrinting((oExp, None))

            dPrintings[(sExp, sPrintName)] = oPrinting

        return dPrintings


DEFAULT_LOOKUP = SimpleLookup()