# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/CliUtils.py
# Compiled at: 2019-12-11 16:37:52
"""
functions to help the CLI programs
"""
from __future__ import print_function
from sqlobject import SQLObjectNotFound
from .core.BaseTables import PhysicalCard, MapPhysicalCardToPhysicalCardSet
from .core.BaseAdapters import IPhysicalCardSet, IAbstractCard
from .core.BaseFilters import PhysicalCardSetFilter, FilterAndBox, PhysicalCardFilter
from .core.FilterParser import FilterParser
from .core.CardSetUtilities import format_cs_list
from .core.DBUtility import make_adapter_caches

def run_filter(sFilter, sCardSet):
    """Run the given filter, returing a dictionary of cards and counts"""
    make_adapter_caches()
    oCardSet = None
    if sCardSet:
        oCardSet = IPhysicalCardSet(sCardSet)
    oParser = FilterParser()
    oFilter = oParser.apply(sFilter).get_filter()
    dResults = {}
    if oCardSet:
        oBaseFilter = PhysicalCardSetFilter(oCardSet.name)
        oJointFilter = FilterAndBox([oBaseFilter, oFilter])
        aResults = oJointFilter.select(MapPhysicalCardToPhysicalCardSet)
        for oCard in aResults:
            oAbsCard = IAbstractCard(oCard)
            dResults.setdefault(oAbsCard, 0)
            dResults[oAbsCard] += 1

    else:
        oBaseFilter = PhysicalCardFilter()
        oJointFilter = FilterAndBox([oBaseFilter, oFilter])
        aResults = oJointFilter.select(PhysicalCard)
        for oCard in aResults:
            oAbsCard = IAbstractCard(oCard)
            dResults.setdefault(oAbsCard, 0)

    return dResults


def print_card_filter_list(dResults, fPrintCard, bDetailed, sEncoding):
    """Print a dictionary of cards returned by runfilter"""
    for oCard in sorted(dResults, key=lambda x: x.name):
        iCnt = dResults[oCard]
        if iCnt:
            print('%3d x %s' % (
             iCnt, oCard.name.encode(sEncoding, 'xmlcharrefreplace')))
        else:
            print(oCard.name.encode(sEncoding, 'xmlcharrefreplace'))
        if bDetailed:
            fPrintCard(oCard, sEncoding)


def print_card_list(sTreeRoot, sEncoding):
    """Print a a list of card sets, handling potential encoding issues
       and a starting point for the tree."""
    if sTreeRoot is not None:
        try:
            oCS = IPhysicalCardSet(sTreeRoot)
            print(' %s' % oCS.name.encode(sEncoding, 'xmlcharrefreplace'))
            print(format_cs_list(oCS, '    ').encode(sEncoding, 'xmlcharrefreplace'))
        except SQLObjectNotFound:
            print('Unable to load card set', sTreeRoot)
            return False

    else:
        print(format_cs_list().encode(sEncoding, 'xmlcharrefreplace'))
    return True


def do_print_card(sCardName, fPrintCard, sEncoding):
    """Print a card, handling possible encoding issues."""
    make_adapter_caches()
    try:
        try:
            oCard = IAbstractCard(sCardName)
        except UnicodeDecodeError as oErr:
            if sEncoding != 'ascii':
                oCard = IAbstractCard(sCardName.decode(sEncoding))
            else:
                print('Unable to interpret card name:')
                print(oErr)
                print('Please specify a suitable --print-encoding')
                return False

        print(oCard.name.encode(sEncoding, 'xmlcharrefreplace'))
        fPrintCard(oCard, sEncoding)
    except SQLObjectNotFound:
        print('Unable to find card %s' % sCardName)
        return False

    return True